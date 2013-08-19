import re

def parseAmount(amountText):
	amount=re.sub('\s|\.|,','',amountText)
	return int(amount)

class LineReader:
	def __init__(self,nCols,nPercentageCols=0,quirks=set()):
		self.nCols=nCols
		self.quirks=quirks
		# compile regexes
		amPattern='\s([+-]?[0-9 ]+[.,]\d)'*self.nCols+'\s\d+[.,]\d\d'*nPercentageCols+'$' # amount (and percentage if needed) pattern
		arPattern='\s(\d{4})\s(\d{6}[0-9а-я])' # article (code) pattern
		self.reLeadNumberLine=re.compile('^((?:\d+\.)+)\s+(.*)$')
		self.reLeadNumberLineWithDotChopped=re.compile('^((?:\d+\.)+\d+)\s+(.*)$')
		if 'undottedNumbers' in self.quirks:
			self.reLeadNumberLineWithDotChopped2=re.compile('^((?:\d+\.)*\d+)\s+(.*)$')
		self.reLineAfterLineWithDotChopped=re.compile('^\.\s+(.*)$')
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

		def readLeadNumberLine(number,rest):
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
				raise Exception('unsupported number')
			return None

		m=self.reTotalLine.match(line)
		if m: # total - has to be before (undotted) lead number
			root=rows[0]
			root['name']='Итого'
			root['amounts']=parseAmounts(m.group,1)
			return nextLine

		if 'undottedNumbers' not in self.quirks:
			m=self.reLeadNumberLineWithDotChopped.match(line)
			if m and nextLine is not None:
				mm=self.reLineAfterLineWithDotChopped.match(nextLine)
				if mm:
					number=m.group(1)+'.'
					rest=m.group(2)
					row=readLeadNumberLine(number,rest)
					if row is not None:
						rows.append(row)
						nextLine=mm.group(1)
						return nextLine
			m=self.reLeadNumberLine.match(line)
			if m:
				number=m.group(1)
				rest=m.group(2)
				if number.count('.')==2:
					mm=self.reLeadNumberLine.match(nextLine)
					if mm: # test if z. follows x.y. - which is wrong
						nnumber=mm.group(1)
						rrest=mm.group(2)
						if nnumber.count('.')==1:
							# append z. to x.y.
							number+=nnumber
							nextLine=rrest
				row=readLeadNumberLine(number,rest)
				if row is not None:
					rows.append(row)
					return nextLine
		else:
			m=self.reLeadNumberLine.match(line)
			if m and nextLine is not None:
				number=m.group(1)
				rest=m.group(2)
				mm=self.reLeadNumberLineWithDotChopped2.match(nextLine)
				if mm:
					number+=mm.group(1)+'.'
					nextLine=mm.group(2)
					row=readLeadNumberLine(number,rest)
					if row is not None:
						rows.append(row)
						return nextLine
			m=self.reLeadNumberLineWithDotChopped2.match(line)
			if m:
				number=m.group(1)+'.'
				rest=m.group(2)
				row=readLeadNumberLine(number,rest)
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
