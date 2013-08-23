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

import record,table

class Spreadsheet:
	def __init__(self,filename,nCols,nPercentageCols=0,allowSlack=False,quirks=set()):
		self.nCols=nCols # this is a number of 'amount' columns in original pdf table - not in generated
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
		self.table=table.TableBuilder(
			self.rows,
			[record.parseAmount(amountText) for amountText in amountTexts],
			self.depthLimit
		)

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
	def getColumnsMetadata(self,stairs):
		r=[
			'number','name','section','article','type'
		]
		if stairs:
			r+=[('amounts',k,(d,)) for k in range(self.nCols) for d in range(self.depthLimit+1)]
		else:
			r+=[('amounts',k,tuple(range(self.depthLimit+1))) for k in range(self.nCols)]
		if self.allowSlack:
			r+=[('amounts',self.nCols-1,'slack')]
		return r

	def write(self,writer,stairs,useSums,rowOffset):
		for row in self.table.rows(self.getColumnsMetadata(stairs),useSums,rowOffset):
			writer.writerow(row)

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

		self.write(csvWriter,stairs,useSums,2)

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
		class Writer:
			def __init__(self):
				self.row=nHeaderRows # private
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

		self.write(Writer(),stairs,useSums,nHeaderRows+1)
		wb.save(filename)
