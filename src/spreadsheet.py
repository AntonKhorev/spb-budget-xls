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

import record

class Entry:
	def __init__(self,iRow,row):
		self.iRow=iRow # -1 for invisible
		self.children={}
		self.number=row.get('number')
		self.name=row.get('name')
		self.article=row.get('article')
		self.section=row.get('section')
		self.type=row.get('type')
		self.amounts=row['amounts']

	def isVisible(self):
		return self.iRow>=0

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
			if n not in self.children: # missing entry of zero sum:
				self.children[n]=Entry(-1,{'amounts':[0]*len(entry.amounts)})
			self.children[n].addLeaf(entry,numberArray)

	def scanRows(self):
		rows=[]
		for child in self.children.values():
			child.scanRows()
			if child.rowSpan is None:
				self.rowSpan=None
				return
			rows.append(child.rowSpan)
		if not rows:
			if self.isVisible():
				self.rowSpan=(self.iRow,self.iRow+1)
				return
			else:
				self.rowSpan=None
				return
		rows.sort()
		if self.isVisible() and self.iRow+1!=rows[0][0]:
			self.rowSpan=None
			return
		for i in range(1,len(rows)):
			if rows[i-1][1]!=rows[i][0]:
				self.rowSpan=None
				return
		if self.isVisible():
			self.rowSpan=(rows[0][0]-1,rows[-1][1])
		else:
			self.rowSpan=(rows[0][0],rows[-1][1])

	def check(self,allowSlack):
		if not self.children:
			return
		sumAmounts=[0]*len(self.amounts)
		for child in self.children.values():
			for k,v in enumerate(child.amounts):
				sumAmounts[k]+=v
		if allowSlack:
			# slack in last column
			slack=self.amounts[-1]-sumAmounts[-1]
			if slack:
				self.slack=slack
				sumAmounts[-1]=self.amounts[-1]
		if sumAmounts!=self.amounts:
			raise Exception('sum(children)!=amount: '+str(sumAmounts)+' != '+str(self.amounts))
		for n,entry in sorted(self.children.items()):
			entry.check(allowSlack)

	def write(self,writer,depth=0):
		def formatAmount(amount):
			a=str(amount)
			return a[:-1]+','+a[-1]

		if self.isVisible():
			if writer.useSums and self.children:
				ams=[]
				for i,v in enumerate(self.amounts):
					# column to sum from
					if writer.stairs:
						columnLetter=chr(ord('F')+depth+1+i*(writer.depthLimit+1))
					else:
						columnLetter=chr(ord('F')+i)
					# formula
					if self.rowSpan is None or not writer.stairs:
						ams.append('='+'+'.join(
							columnLetter+writer.strrow(entry.iRow) for n,entry in sorted(self.children.items()) if entry.isVisible()
						))
					else:
						ams.append('=SUM('+columnLetter+writer.strrow(self.rowSpan[0]+1)+':'+columnLetter+writer.strrow(self.rowSpan[1]-1)+')')
					if i==len(self.amounts)-1 and hasattr(self,'slack'):
						if writer.stairs:
							slackColumnLetter=chr(ord('F')+(i+1)*(writer.depthLimit+1))
						else:
							slackColumnLetter=chr(ord('F')+i+1)
						ams[-1]+='+'+slackColumnLetter+writer.strrow(self.iRow)
			else:
				ams=[formatAmount(v) for v in self.amounts]
			if writer.stairs:
				amList=list(itertools.chain.from_iterable([None]*depth+[am]+[None]*(writer.depthLimit-depth) for am in ams))
			else:
				amList=ams
			if hasattr(self,'slack'):
				amList+=[formatAmount(self.slack)]
			writer.writerow([self.number,self.name,self.section,self.article,self.type]+amList)

		for n,entry in sorted(self.children.items()):
			entry.write(writer,depth+1)

	def __str__(self):
		return 'number:'+str(self.number)+'; name:'+str(self.name)+'; amounts:'+str(self.amounts)

class Spreadsheet:
	def __init__(self,filename,nCols,nPercentageCols=0,allowSlack=False,quirks=set()):
		self.nCols=nCols
		self.allowSlack=allowSlack
		self.amountHeader=['Сумма (тыс. руб.)']*self.nCols
		self.documentTitle='Приложение к Закону Санкт-Петербурга о бюджете'
		self.tableTitle='Ведомственная структура расходов бюджета Санкт-Петербурга'

		# read file
		f=open(filename,encoding='utf8')
		lines=f.readlines()
		f.close()

		# parse
		rb=record.RecordBuilder(self.nCols,nPercentageCols,quirks=quirks)
		self.rows=[{},None]
		for i,line in enumerate(lines):
			nextLine=lines[i+1] if i<len(lines)-1 else None
			nextLine=rb.read(self.rows,line,nextLine)
			if i<len(lines)-1:
				lines[i+1]=nextLine

	def setAmountHeader(self,header):
		self.amountHeader=header

	def setDocumentTitle(self,documentTitle):
		self.documentTitle=documentTitle

	def setTableTitle(self,tableTitle):
		self.tableTitle=tableTitle

	def build(self,depthLimit,amountTexts):
		self.depthLimit=depthLimit

		# make entries
		iRow=0
		for i,row in enumerate(self.rows):
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

		# check amounts / calculate slack
		self.root.check(self.allowSlack)
		for i,amountText in enumerate(amountTexts):
			self.root.checkAmount(record.parseAmount(amountText),i)

	# private
	def getHeaderRow(self,stairs):
		return [
			'Номер','Наименование','Код раздела','Код целевой статьи','Код вида расходов'
		]+(
			list(itertools.chain.from_iterable([v]+[None]*self.depthLimit for v in self.amountHeader)) if stairs
			else self.amountHeader
		)+(
			['Поправка на округление (тыс. руб.)'] if self.allowSlack
			else []
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
		ws.col(0).width=256*10
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
