import re

def parseAmount(amountText):
	amount=re.sub('\s|\.|,','',amountText)
	return int(amount)

class RecordBuilder:
	def __init__(self,nCols,nPercentageCols=0,quirks=set()):
		self.nCols=nCols
		# compile regexes
		nmPattern='^(?P<name>.*?)'
		amPattern='\s([+-]?[0-9 ]+[.,]\d)'*self.nCols+'\s-?\d+[.,]\d\d'*nPercentageCols+'$' # amount (and percentage if needed) pattern
		if 'splitSection' in quirks:
			arPattern='\s(?P<section>\d\d\s+\d\d)'
		else:
			arPattern='\s(?P<section>\d{4})'
		arPattern+='\s(?P<article>\d\d[0-9а-яА-Я]\d\d[0-9а-яА-Я][0-9а-яА-Я])' # article (code) pattern
		atPattern='\s(?P<type>\d{3})' # type pattern
		if 'OSGUcode' in quirks:
			atPattern+='\s(?P<OSGU>\d{3})'
		if 'econcode' in quirks:
			atPattern+='\s(?P<econ>\d{3})'
		self.reFirstRecordLine=re.compile('^((?:\d\.?)+)\s+(.*)$')
		self.reNextRecordLine=re.compile('^(\.(?:\d\.?)*|(?:\d\.?)+)(?:\s+(.*))?$')
		if 'undottedNumbers' not in quirks:
			self.reNumber=re.compile('^(?:\d+\.){1,'+str(4 if 'depth4' in quirks else 3)+'}$')
			self.dotNumber=lambda number: number
		else:
			self.reNumber=re.compile('^\d+(?:\.\d+){,'+str(3 if 'depth4' in quirks else 2)+'}$')
			self.dotNumber=lambda number: number+'.'
		self.reLineEndingForDepth={
			1:re.compile(nmPattern+amPattern),
			2:re.compile(nmPattern+arPattern+amPattern),
			3:re.compile(nmPattern+arPattern+atPattern+amPattern),
		}
		if 'depth4' in quirks:
			self.reLineEndingForDepth[4]=self.reLineEndingForDepth[3]
		if 'unmarkedTotal' in quirks:
			self.reTotalLine=re.compile('^(\d\d\d \d\d\d \d\d\d.\d)$')
		else:
			self.reTotalLine=re.compile('^\s?Итого:'+amPattern)
		self.reNewPageLine=re.compile('^\d+\s+Приложение|^Показатели расходов бюджета Санкт-Петербурга за')

	# rows:
	#	dictionary with row data
	#	None for page break
	#	init with: [<root>,None]
	# nextLine is needed to see parts of number
	#	None if reached eof
	# complete number is needed to scan the rest of line
	def read(self,rows,line,nextLine,nsc=None):

		def appendName(name1,name2):
			name2=name2.strip()
			name2=re.sub(r' ,',r',',name2)
			name2=re.sub(r'(^| )" ',r'\1"',name2) # before double space
			name2=re.sub(r' {2,}',r' ',name2) # double space
			name2=re.sub(r'Ы ([А-ЗЙ-Я])',r'Ы\1',name2) # ЖИЛИЩНЫ Й -> ЖИЛИЩНЫЙ, СРЕДЫ И -> СРЕДЫ И
			if name1 is None:
				return name2
			else:
				if len(name1)>=2 and (name1[-1]!='-' or name1[-2]==' '):
					name1+=' '
				return name1+name2

		def makeName(name):
			return appendName(None,name)

		def parseAmounts(group,offset):
			return [parseAmount(group(i+offset)) for i in range(self.nCols)]

		def readFirstRecordLine(number,rest):
			number=self.dotNumber(number)
			nc=number.count('.') # depth: 1 = x. ; 2 = x.y. ; 3 = x.y.z.
			if nc not in self.reLineEndingForDepth:
				raise Exception('unsupported number '+number)
			m=self.reLineEndingForDepth[nc].match(rest)
			if m:
				row=m.groupdict()
				if 'section' in row:
					row['section']=row['section'][:2]+row['section'][-2:]
				row['name']=makeName(row['name'])
				row['number']=number
				row['amounts']=parseAmounts(m.group,len(row))
				return row
			return None

		m=self.reTotalLine.match(line)
		if m: # total - has to be before (undotted) lead number
			root=rows[0]
			root['name']='Итого'
			root['amounts']=parseAmounts(m.group,1)
			return nextLine

		m=self.reFirstRecordLine.match(line)
		if m:
			number1=m.group(1)
			rest1=m.group(2)
			mm=self.reNextRecordLine.match(nextLine)
			if mm and not self.reNewPageLine.match(nextLine):
				number2=mm.group(1)
				rest2=mm.group(2)
				number=number1+number2
				if (
					self.reNumber.match(number) and
					(not (nsc and rows[-1] and 'number' in rows[-1]) or nsc.checkPair(rows[-1]['number'],number)) and
					(not self.reNumber.match(number2) or readFirstRecordLine(number2,rest2) is None)
				):
					row=readFirstRecordLine(number,rest1)
					if row is not None:
						rows.append(row)
						return rest2
			if self.reNumber.match(number1):
				row=readFirstRecordLine(number1,rest1)
				if row is not None:
					rows.append(row)
					return nextLine

		if self.reNewPageLine.match(line): # new page
			rows.append(None)
			return nextLine
		if rows[-1] is not None: # next line of name
			row=rows[-1]
			row['name']=appendName(row['name'],line)
		return nextLine
