import re

class LineReader:
	def __init__(self,nCols):
		self.nCols=nCols
		# compile regexes
		amPattern='\s([+-]?[0-9 ]+[.,]\d)'*self.nCols+'$' # amount pattern
		arPattern='\s(\d{4})\s(\d{6}[0-9а-я])' # article (code) pattern
		self.reLeadNumberLine=re.compile('^((?:\d+\.)+)\s+(.*)$')
		self.reLeadNumberLineWithDotChopped=re.compile('^((?:\d+\.)+\d+)\s+(.*)$')
		self.reLineAfterLineWithDotChopped=re.compile('^\.\s+(.*)$')
		self.reLineEndingDepth1=re.compile('^(.*?)'+amPattern)
		self.reLineEndingDepth2=re.compile('^(.*?)'+arPattern+amPattern)
		self.reLineEndingDepth3=re.compile('^(.*?)'+arPattern+'\s(\d{3})'+amPattern)
		self.reTotalLine=re.compile('^(Итого):'+amPattern)
		self.reNewPageLine=re.compile('^\d+\s+Приложение')

	# rows:
	#	dictionary with row data
	#	None for page break
	#	init with: [<root>,None]
	# nextLine is needed to see parts of number
	# complete number is needed to scan the rest of line
	def read(self,rows,line,nextLine):
		return nextLine # TODO
