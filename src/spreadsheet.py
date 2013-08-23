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
	def __init__(self,filename,nCols,nPercentageCols=0,quirks=set()):
		self.nCols=nCols # this is a number of 'amount' columns in original pdf table - not in generated
		self.amountHeader=['Сумма (тыс. руб.)']*self.nCols
		self.documentTitle='Приложение к Закону Санкт-Петербурга о бюджете'
		self.tableTitle='Ведомственная структура расходов бюджета Санкт-Петербурга'
		self.slackHeader={}

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

	def setSlackHeader(self,header):
		self.slackHeader=header

	def build(self,depthLimit,amountTexts):
		self.depthLimit=depthLimit
		self.table=table.TableBuilder(
			self.rows,
			[record.parseAmount(amountText) for amountText in amountTexts],
			self.depthLimit
		)

	# private
	def makeColumnsMetadata(self,stairs):
		metadata=[
			{'text':'Номер',		'subtext':None,'span':1,'id':'number'},
			{'text':'Наименование',		'subtext':None,'span':1,'id':'name'},
			{'text':'Код раздела',		'subtext':None,'span':1,'id':'section'},
			{'text':'Код целевой статьи',	'subtext':None,'span':1,'id':'article'},
			{'text':'Код вида расходов',	'subtext':None,'span':1,'id':'type'},
		]
		for k in range(self.nCols):
			if stairs:
				metadata+=[{
					'text':self.amountHeader[k],
					'subtext':'глубина '+str(d) if d else 'итого',
					'span':(self.depthLimit+1),
					'id':('amounts',k,(d,)),
				} for d in range(self.depthLimit+1)]
			else:
				metadata+=[{
					'text':self.amountHeader[k],
					'subtext':None,
					'span':1,
					'id':('amounts',k,tuple(range(self.depthLimit+1)))
				}]
			if k in self.slackHeader:
				metadata+=[{
					'text':self.slackHeader[k],
					'subtext':None,
					'span':1,
					'id':('amounts',k,'slack')
				}]
		return metadata

	def write(self,writer,stairs,useSums,rowOffset):
		for row in self.table.rows([
			m['id'] for m in self.makeColumnsMetadata(stairs)
		],useSums,rowOffset):
			writer.writerow(row)

	def writeCsv(self,filename,stairs,useSums):
		metadata=self.makeColumnsMetadata(stairs)
		csvWriter=csv.writer(open(filename,'w',newline='',encoding='utf8'),quoting=csv.QUOTE_NONNUMERIC)
		csvWriter.writerow([m['text']+(' ('+m['subtext']+')' if m['subtext'] is not None else '') for m in metadata])
		self.write(csvWriter,stairs,useSums,2)

	def writeXls(self,filename,delta,stairs,useSums=True):
		wb=xlwt.Workbook()
		# ws=wb.add_sheet('Ведомственная структура расходов') # can't use Russian?
		ws=wb.add_sheet('expenditures')
		metadata=self.makeColumnsMetadata(stairs)

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

		# table header
		nHeaderRows=3
		ws.set_panes_frozen(True)
		ws.set_horz_split_pos(nHeaderRows)
		ws.row(0).height=ws.row(1).height=400
		ws.merge(0,0,0,len(metadata)-1)
		ws.write(0,0,self.documentTitle,styleDocumentTitle)
		ws.merge(1,1,0,len(metadata)-1)
		ws.write(1,0,self.tableTitle,styleTableTitle)

		# columns header
		ws.row(nHeaderRows-1).height=1200
		columnTypes={
			'number':	{'width':10,	'style':styleHeader},
			'name':		{'width':100,	'style':styleHeader},
			'section':	{'width':5,	'style':styleThinHeader},
			'article':	{'width':8,	'style':styleThinHeader},
			'type':		{'width':4,	'style':styleVeryThinHeader},
		}
		amountType=		{'width':15,	'style':styleHeader}
		skip=0
		for i,m in enumerate(metadata):
			if skip>0:
				skip-=1
				continue
			r=nHeaderRows-1
			if m['span']>1:
				ws.merge(r,r,i,i+m['span']-1)
				skip=m['span']-1
			if m['id'] in columnTypes:
				ct=columnTypes[m['id']]
				ws.col(i).width=256*ct['width']
				style=ct['style']
			elif type(m['id']) is tuple:
				ws.col(i).width=256*amountType['width']
				style=amountType['style']
			ws.write(r,i,m['text'],style)

		# data
		class Writer:
			def __init__(self):
				self.row=nHeaderRows # private
			def writerow(self,cells):
				for i,cell in enumerate(cells):
					if cell is None:
						continue
					if type(metadata[i]['id']) is tuple:
						if cell[0]=='=':
							ws.write(self.row,i,xlwt.Formula(cell[1:]),styleAmount)
						else:
							ws.write(self.row,i,float(cell.replace(',','.')),styleAmount)
					else:
						ws.write(self.row,i,cell)
				self.row+=1

		self.write(Writer(),stairs,useSums,nHeaderRows+1)
		wb.save(filename)
