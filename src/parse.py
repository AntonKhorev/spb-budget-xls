# for writeXls():
#	need this fork of this port of xls writer
#	https://bitbucket.org/luensdorf/xlwt3
# 	TODO other libs to consider:
#		http://pythonhosted.org/openpyxl/
#		http://www.python-excel.org/
#		https://pypi.python.org/pypi/xlwt3

import os.path, glob
import re, csv
import itertools
import xlwt3 as xlwt

class Entry:
	def __init__(self,row):
		self.row=row
		self.children={}
		self.number=self.name=self.article=self.section=self.type=None
		self.amounts={}

	def appendName(self,name):
		name=name.strip()
		name=re.sub(r'" ([А-Я])',r'"\1',name) # " Дирекция -> "Дирекция
		name=re.sub(r'Ы ([А-Я])',r'Ы\1',name) # ЖИЛИЩНЫ Й -> ЖИЛИЩНЫЙ
		if self.name is None:
			self.name=name
		else:
			if self.name[-1]!='-' or self.name[-2]==' ':
				self.name+=' '
			self.name+=name

	def parseAmount(self,amountText):
		amount=re.sub('\s|\.|,','',amountText)
		return int(amount)

	def addAmount(self,amountText,key=0):
		self.amounts[key]=self.parseAmount(amountText)

	def checkAmount(self,amountText,key=0):
		amount=self.parseAmount(amountText)
		if amount!=self.amounts[key]:
			raise Exception("amount doesn't match")

	def addLeaf(self,entry,number):
		n=number.pop(0)
		if len(number)==0:
			if n in self.children:
				raise Exception('duplicate entry')
			self.children[n]=entry
		else:
			if n not in self.children:
				raise Exception('child not found')
			self.children[n].addLeaf(entry,number)

	def formatAmount(self,amount):
		a=str(amount)
		return a[:-1]+','+a[-1]

	def scanRows(self):
		if not self.children:
			self.rowSpan=(self.row,self.row+1)
			return
		rows=[]
		for child in self.children.values():
			child.scanRows()
			if child.rowSpan is None:
				self.rowSpan=None
				return
			rows.append(child.rowSpan)
		rows.sort()
		if self.row+1!=rows[0][0]:
			self.rowSpan=None
			return
		for i in range(1,len(rows)):
			if rows[i-1][1]!=rows[i][0]:
				self.rowSpan=None
				return
		self.rowSpan=(rows[0][0]-1,rows[-1][1])

	def check(self):
		if not self.children:
			return
		sumAmounts={}
		for child in self.children.values():
			for k,v in child.amounts.items():
				if k not in sumAmounts:
					sumAmounts[k]=0
				sumAmounts[k]+=v
		if sumAmounts!=self.amounts:
			raise Exception('sum(children)!=amount: '+str(sumAmounts)+' != '+str(self.amounts))
		for n,entry in sorted(self.children.items()):
			entry.check()

	def checkAmounts(self,amountTexts):
		for i,amountText in enumerate(amountTexts):
			self.checkAmount(amountText,i)

	def write(self,writer,depth=0):
		if writer.useSums and self.children:
			ams=[]
			for i,(k,v) in enumerate(sorted(self.amounts.items())):
				# column to sum from
				if writer.stairs:
					columnLetter=chr(ord('F')+depth+1+i*(writer.depthLimit+1))
				else:
					columnLetter=chr(ord('F')+i)
				# formula
				if self.rowSpan is None or not writer.stairs:
					ams.append('='+'+'.join(columnLetter+writer.strrow(entry.row) for n,entry in sorted(self.children.items())))
				else:
					ams.append('=SUM('+columnLetter+writer.strrow(self.rowSpan[0]+1)+':'+columnLetter+writer.strrow(self.rowSpan[1]-1)+')')
		else:
			ams=[self.formatAmount(v) for k,v in sorted(self.amounts.items())]
		if writer.stairs:
			amList=list(itertools.chain.from_iterable([None]*depth+[am]+[None]*(writer.depthLimit-depth) for am in ams))
		else:
			amList=ams
		writer.writerow([self.number,self.name,self.section,self.article,self.type]+amList)
		for n,entry in sorted(self.children.items()):
			entry.write(writer,depth+1)

	def __str__(self):
		return 'number:'+str(self.number)+'; name:'+str(self.name)+'; amounts:'+str(self.amounts)

class Spreadsheet:
	def __init__(self,nCols,depthLimit):
		self.nCols=nCols
		self.row=0
		self.depthLimit=depthLimit
		self.root=Entry(self.row)
		self.amountHeader=['Сумма (тыс. руб.)']*self.nCols
		self.documentTitle='Приложение к Закону Санкт-Петербурга о бюджете'
		self.tableTitle='Ведомственная структура расходов бюджета Санкт-Петербурга'

	# private
	def makeEntry(self,numberStr):
		number=[int(n) for n in numberStr.split('.') if n!='']
		if len(number)>self.depthLimit:
			return Entry(-1) # throwaway entry
		self.row+=1
		entry=Entry(self.row)
		entry.number=numberStr
		self.root.addLeaf(entry,number)
		return entry

	def read(self,filename):
		entry=None

		amPattern='\s([+-]?[0-9 ]+[.,]\d)'*self.nCols+'$' # amount pattern
		arPattern='\s(\d{4})\s(\d{6}[0-9а-я])' # article (code) pattern
		reLeadNumberLine=re.compile('^((?:\d+\.)+)\s+(.*)$')
		reLeadNumberLineWithDotChopped=re.compile('^((?:\d+\.)+\d+)\s+(.*)$')
		reLineAfterLineWithDotChopped=re.compile('^\.\s+(.*)$')
		reLineEndingDepth1=re.compile('^(.*?)'+amPattern)
		reLineEndingDepth2=re.compile('^(.*?)'+arPattern+amPattern)
		reLineEndingDepth3=re.compile('^(.*?)'+arPattern+'\s(\d{3})'+amPattern)
		reTotalLine=re.compile('^(Итого):'+amPattern)
		reNewPageLine=re.compile('^\d+\s+Приложение')

		def readLeadNumberLine(number,rest):
			nc=number.count('.') # depth: 1 = x. ; 2 = x.y. ; 3 = x.y.z.
			if nc==1:
				m=reLineEndingDepth1.match(rest)
				if m:
					entry=self.makeEntry(number)
					entry.appendName(m.group(1))
					for i in range(self.nCols):
						entry.addAmount(m.group(i+2),i)
					return entry
			elif nc==2:
				m=reLineEndingDepth2.match(rest)
				if m:
					entry=self.makeEntry(number)
					entry.appendName(m.group(1))
					entry.section=m.group(2)
					entry.article=m.group(3)
					for i in range(self.nCols):
						entry.addAmount(m.group(i+4),i)
					return entry
			elif nc==3:
				m=reLineEndingDepth3.match(rest)
				if m:
					entry=self.makeEntry(number)
					entry.appendName(m.group(1))
					entry.section=m.group(2)
					entry.article=m.group(3)
					entry.type=m.group(4)
					for i in range(self.nCols):
						entry.addAmount(m.group(i+5),i)
					return entry
			else:
				raise Exception('unsupported number')
			return None

		f=open(filename,encoding='utf8')
		lines=f.readlines()
		f.close()

		for i,line in enumerate(lines):
			m=reLeadNumberLineWithDotChopped.match(line)
			if m and i<len(lines)-1:
				mm=reLineAfterLineWithDotChopped.match(lines[i+1])
				if mm:
					number=m.group(1)+'.'
					rest=m.group(2)
					e=readLeadNumberLine(number,rest)
					if e is not None:
						entry=e
						lines[i+1]=mm.group(1)
						continue
			m=reLeadNumberLine.match(line)
			if m:
				number=m.group(1)
				rest=m.group(2)
				e=readLeadNumberLine(number,rest)
				if e is not None:
					entry=e
					continue
			m=reTotalLine.match(line)
			if m: # total
				self.root.name=m.group(1)
				for i in range(self.nCols):
					self.root.addAmount(m.group(i+2),i)
				continue
			if reNewPageLine.match(line): # new page
				entry=None
				continue
			if entry: # next line of name
				entry.appendName(line)
		self.root.scanRows()

	def check(self,amountTexts):
		self.root.check()
		self.root.checkAmounts(amountTexts)

	def setAmountHeader(self,header):
		self.amountHeader=header

	def setDocumentTitle(self,documentTitle):
		self.documentTitle=documentTitle

	def setTableTitle(self,tableTitle):
		self.tableTitle=tableTitle

	# private
	def getHeaderRow(self,stairs):
		return [
			'Номер','Наименование','Код раздела','Код целевой статьи','Код вида расходов'
		]+(
			list(itertools.chain.from_iterable([v]+[None]*self.depthLimit for v in self.amountHeader)) if stairs
			else self.amountHeader
		)

	def writeCsv(self,filename,stairs,useSums):
		csvWriter=csv.writer(open(filename,'w',newline='',encoding='utf8'),quoting=csv.QUOTE_NONNUMERIC)
		csvWriter.writerow(self.getHeaderRow(stairs))

		depthLimit=self.depthLimit
		class Writer:
			def __init__(self):
				self.stairs=stairs
				self.useSums=useSums
				self.depthLimit=depthLimit
			def strrow(self,row):
				return str(row+2) # row 1 for header
			def writerow(self,cells):
				csvWriter.writerow(cells)

		self.root.write(Writer())

	def writeXls(self,filename,delta,stairs,useSums=True):
		wb=xlwt.Workbook()
		# ws=wb.add_sheet('Ведомственная структура расходов') # can't use Russian?
		ws=wb.add_sheet('expenditures')

		# split panes
		nHeaderRows=3
		ws.set_panes_frozen(True)
		ws.set_horz_split_pos(nHeaderRows)

		# column widths
		ws.col(0).width=256*8
		ws.col(1).width=256*100
		ws.col(2).width=256*5
		ws.col(3).width=256*8
		ws.col(4).width=256*4
		for i in range(5,5+((self.depthLimit if stairs else 0)+1)*self.nCols):
			ws.col(i).width=256*15

		# row heights
		ws.row(0).height=ws.row(1).height=400
		ws.row(nHeaderRows-1).height=1200

		# colspans
		colspan=len(self.getHeaderRow(stairs))-1
		ws.merge(0,0,0,colspan)
		ws.merge(1,1,0,colspan)
		if stairs:
			for i in range(self.nCols):
				c1=5+i*(self.depthLimit+1)
				c2=5+i*(self.depthLimit+1)+self.depthLimit
				r=nHeaderRows-1
				ws.merge(r,r,c1,c2)

		# styles
		styleDocumentTitle=xlwt.easyxf('font: height 240')
		styleTableTitle=xlwt.easyxf('font: bold on, height 240')
		styleHeader=xlwt.easyxf('font: bold on; align: wrap on')
		styleThinHeader=xlwt.easyxf('font: bold on, height 180; align: wrap on')
		styleVeryThinHeader=xlwt.easyxf('font: height 140; align: wrap on')
		# для русского в числовом формате НУЖНО писать ',' вместо ' ' и '.' вместо ','
		if delta:
			styleAmount=xlwt.easyxf(num_format_str="+#,##0.0;-#,##0.0;0.0")
		else:
			styleAmount=xlwt.easyxf(num_format_str='#,##0.0')

		# headers
		ws.write(0,0,self.documentTitle,styleDocumentTitle)
		ws.write(1,0,self.tableTitle,styleTableTitle)
		for i,cell in enumerate(self.getHeaderRow(stairs)):
			if cell is None:
				continue
			if 2<=i<=3:
				style=styleThinHeader
			elif i==4:
				style=styleVeryThinHeader
			else:
				style=styleHeader
			ws.write(nHeaderRows-1,i,cell,style)

		# data
		depthLimit=self.depthLimit
		class Writer:
			def __init__(self):
				self.row=nHeaderRows # private
				self.stairs=stairs
				self.useSums=useSums
				self.depthLimit=depthLimit
			def strrow(self,row):
				return str(row+nHeaderRows+1) # rows 1..nHeaderRows for header
			def writerow(self,cells):
				for i,cell in enumerate(cells):
					if cell is None:
						continue
					if i>=5 and cell[0]=='=':
						ws.write(self.row,i,xlwt.Formula(cell[1:]),styleAmount)
					elif i>=5:
						ws.write(self.row,i,float(cell.replace(',','.')),styleAmount)
					else:
						ws.write(self.row,i,cell)
				self.row+=1

		self.root.write(Writer())
		wb.save(filename)
