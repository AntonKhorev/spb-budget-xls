# for writeXls():
#	need this fork of this port of xls writer
#	https://bitbucket.org/luensdorf/xlwt3
# 	TODO other libs to consider:
#		http://pythonhosted.org/openpyxl/
#		http://www.python-excel.org/
#		https://pypi.python.org/pypi/xlwt3

import sys,itertools
import csv
import xlwt3 as xlwt

import reader

class Entry:
	def __init__(self,iRow,row):
		self.iRow=iRow
		self.children={}
		self.number=row.get('number')
		self.name=row.get('name')
		self.article=row.get('article')
		self.section=row.get('section')
		self.type=row.get('type')
		self.amounts={i:amount for i,amount in enumerate(row['amounts'])}

	def checkAmount(self,amount,key=0):
		if amount!=self.amounts[key]:
			raise Exception("amount doesn't match")

	def addLeaf(self,entry,numberArray):
		n=numberArray.pop(0)
		if len(numberArray)==0:
			if n in self.children:
				raise Exception('duplicate entry')
			self.children[n]=entry
		else:
			if n not in self.children:
				raise Exception('child not found')
			self.children[n].addLeaf(entry,numberArray)

	def scanRows(self):
		if not self.children:
			self.rowSpan=(self.iRow,self.iRow+1)
			return
		rows=[]
		for child in self.children.values():
			child.scanRows()
			if child.rowSpan is None:
				self.rowSpan=None
				return
			rows.append(child.rowSpan)
		rows.sort()
		if self.iRow+1!=rows[0][0]:
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

	def write(self,writer,depth=0):
		def formatAmount(amount):
			a=str(amount)
			return a[:-1]+','+a[-1]

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
					ams.append('='+'+'.join(columnLetter+writer.strrow(entry.iRow) for n,entry in sorted(self.children.items())))
				else:
					ams.append('=SUM('+columnLetter+writer.strrow(self.rowSpan[0]+1)+':'+columnLetter+writer.strrow(self.rowSpan[1]-1)+')')
		else:
			ams=[formatAmount(v) for k,v in sorted(self.amounts.items())]
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
		self.depthLimit=depthLimit
		self.amountHeader=['Сумма (тыс. руб.)']*self.nCols
		self.documentTitle='Приложение к Закону Санкт-Петербурга о бюджете'
		self.tableTitle='Ведомственная структура расходов бюджета Санкт-Петербурга'

	def read(self,filename):
		# read file
		f=open(filename,encoding='utf8')
		lines=f.readlines()
		f.close()

		# parse
		lr=reader.LineReader(self.nCols)
		rows=[{},None]
		for i,line in enumerate(lines):
			nextLine=lines[i+1] if i<len(lines)-1 else None
			nextLine=lr.read(rows,line,nextLine)
			if i<len(lines)-1:
				lines[i+1]=nextLine

		# make entries
		iRow=0
		for i,row in enumerate(rows):
			if row is None:
				continue
			entry=Entry(iRow,row)
			if i==0:
				self.root=entry
			else:
				numberArray=[int(n) for n in row['number'].split('.') if n!='']
				if len(numberArray)>self.depthLimit:
					continue
				try:
					self.root.addLeaf(entry,numberArray)
				except Exception as e:
					tb=sys.exc_info()[2]
					raise Exception(str(e)+' in entry number '+row['number']).with_traceback(tb)
			iRow+=1

		# make rowspans
		self.root.scanRows()

	def check(self,amountTexts):
		self.root.check()
		for i,amountText in enumerate(amountTexts):
			self.root.checkAmount(reader.parseAmount(amountText),i)

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
