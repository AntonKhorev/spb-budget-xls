import re

def parseAmount(amountText):
	amount=re.sub('\s|\.|,','',amountText)
	return int(amount)

class RecordBuilder:
	def __init__(self,nCols,nPercentageCols=0,quirks=set()):
		self.nCols=nCols
		# compile regexes
		amPattern='\s([+-]?[0-9 ]+[.,]\d)'*self.nCols+'\s\d+[.,]\d\d'*nPercentageCols+'$' # amount (and percentage if needed) pattern
		arPattern='\s(\d{4})\s(\d{6}[0-9а-я])' # article (code) pattern
		self.reFirstRecordLine=re.compile('^((?:\d\.?)+)\s+(.*)$')
		self.reNextRecordLine=re.compile('^(\.?(?:\d\.?)+)\s+(.*)$')
		if 'undottedNumbers' not in quirks:
			self.reNumber=re.compile('^(?:\d+\.){1,3}$')
			self.dotNumber=lambda number: number
		else:
			self.reNumber=re.compile('^\d+(?:\.\d+){,2}$')
			self.dotNumber=lambda number: number+'.'
		self.reLineEndingDepth1=re.compile('^(.*?)'+amPattern)
		self.reLineEndingDepth2=re.compile('^(.*?)'+arPattern+amPattern)
		self.reLineEndingDepth3=re.compile('^(.*?)'+arPattern+'\s(\d{3})'+amPattern)
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
	def read(self,rows,line,nextLine):

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
			if nc==1:
				m=self.reLineEndingDepth1.match(rest)
				if m:
					return {
						'number':number,
						'name':makeName(m.group(1)),
						'amounts':parseAmounts(m.group,2),
					}
			elif nc==2:
				m=self.reLineEndingDepth2.match(rest)
				if m:
					return {
						'number':number,
						'name':makeName(m.group(1)),
						'section':m.group(2),
						'article':m.group(3),
						'amounts':parseAmounts(m.group,4),
					}
			elif nc==3:
				m=self.reLineEndingDepth3.match(rest)
				if m:
					return {
						'number':number,
						'name':makeName(m.group(1)),
						'section':m.group(2),
						'article':m.group(3),
						'type':m.group(4),
						'amounts':parseAmounts(m.group,5),
					}
			else:
				raise Exception('unsupported number '+number)
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
			if mm:
				number2=mm.group(1)
				rest2=mm.group(2)
				number=number1+number2
				if self.reNumber.match(number) and (not self.reNumber.match(number2) or readFirstRecordLine(number2,rest2) is None):
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