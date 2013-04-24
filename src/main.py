# basic types
# filenames are always absolute/ready to be read

import os.path
import io
import zipfile
import subprocess

import data,parse

# приложения, которые парсим
class Document:
	def __init__(self,law,data):
		# fix data
		if isinstance(data['forYear'],(str,int)):
			data['forYear']=(data['forYear'],)
		data['forYear']=tuple(str(y) for y in data['forYear'])
		if isinstance(data['total'],(str,int)):
			data['total']=(data['total'],)
		if 'delta' not in data:
			data['delta']=False
		# init
		self.law=law
		self.forYears=data['forYear']
		self.code=self.law.code+'-'+','.join(self.forYears)
		self.pdfFilename=self.law.environment.rootPath+'/pdf/'+self.code+'.pdf'
		self.txtFilename=self.law.environment.rootPath+'/txt/'+self.code+'.txt'
		self.zipContents=data['zipContents']
		self.totals=data['total']
		if len(self.forYears)!=len(self.totals):
			raise Exception('invalid number of columns')
		self.nCols=len(self.totals)
		self.delta=data['delta']
		self.appendixNumber=data['appendixNumber']
		self.title=data['title']
	def hasPdf(self):
		return os.path.isfile(self.pdfFilename)
	def writePdf(self):
		# attempt to read before opening pdfFile - otherwise might get zero-length file on error
		bytes=None
		for s in self.zipContents.split('/'):
			if bytes is None:
				zipFile=zipfile.ZipFile(law.zipFilename)
			else:
				zipFile=zipfile.ZipFile(io.BytesIO(bytes))
			bytes=zipFile.read(s)
			zipFile.close()
		# write pdf
		pdfFile=open(self.pdfFilename,'wb')
		pdfFile.write(bytes)
		pdfFile.close()
	def hasTxt(self):
		return os.path.isfile(self.txtFilename)
	def writeTxt(self):
		status=subprocess.call(['java','-jar',self.law.environment.pdfboxFilename,'ExtractText','-encoding','UTF-8','-sort',self.pdfFilename,self.txtFilename])
		if status!=0:
			raise Exception('external command failure')
	def getFilenameParensPart(self,depth,stairs,sums):
		return '('+str(depth)+(',stairs' if stairs else '')+(',sums' if sums else '')+')'
	def getCsvFilename(self,depth,stairs,sums):
		return self.law.environment.rootPath+'/csv/'+self.code+self.getFilenameParensPart(depth,stairs,sums)+'.csv'
	def getXlsFilename(self,depth,stairs):
		sums=True
		return self.law.environment.rootPath+'/xls/'+self.code+self.getFilenameParensPart(depth,stairs,sums)+'.xls'
	def hasCsvsAndXlss(self):
		for depth in range(1,4):
			for stairs in (False,True):
				for sums in (False,True):
					if not os.path.isfile(self.getCsvFilename(depth,stairs,sums)):
						return False
				if not os.path.isfile(self.getXlsFilename(depth,stairs)):
					return False
		return True
	def writeCsvsAndXlss(self):
		header=[('Изменение суммы' if self.delta else 'Сумма')+' на '+year+' г. (тыс. руб.)' for year in self.forYears]
		for depth in range(1,4):
			spreadsheet=parse.Spreadsheet(self.nCols,depth)
			spreadsheet.read(self.txtFilename)
			spreadsheet.check(self.totals)
			spreadsheet.setDocumentTitle('Приложение '+str(self.appendixNumber)+' к Закону Санкт-Петербурга «'+self.law.title+'»')
			spreadsheet.setTableTitle(self.title)
			spreadsheet.setAmountHeader(header)
			for stairs in (False,True):
				for sums in (False,True):
					csvFilename=self.getCsvFilename(depth,stairs,sums)
					spreadsheet.writeCsv(csvFilename,stairs,sums)
				xlsFilename=self.getXlsFilename(depth,stairs)
				spreadsheet.writeXls(xlsFilename,self.delta,stairs)

# закон или законопроект, в к-рый входит несколько приложений - с ними отдельно разбираться
class Law:
	def __init__(self,environment,data):
		# year = на какой год (первый из (трёх) годов) (FIXME update)
		# date = дата опубликования
		# viewUrl = url для просмотра
		# downloadUrl = url для скачивания
		#	из него будет делаться путь к скачанным файлам в /zip
		# version = (FIXME update)
		#	0 - исходный закон/проект
		#	1,2,3,... - n-я корректировка (пока была только одна корректировка, даты есть только для 2013)
		#		бывает и больше корректировок
		#	-1 - закон об исполнении (его проекта нет, в зипе только приложения)
		if 'documents' not in data:
			data['documents']=[]
		self.environment=environment
		self.code=data['code']
		if not data['downloadUrl'].startswith(self.environment.rootUrl):
			raise Exception('invalid download url')
		self.zipFilename=self.environment.rootPath+'/zip/'+data['downloadUrl'][len(self.environment.rootUrl):]
		self.title=data['title']
		self.documents=(Document(self,documentData) for documentData in data['documents'])
	def hasZip(self):
		return os.path.isfile(self.zipFilename)

class Environment:
	def __init__(self,data):
		self.rootPath=os.path.realpath(
			os.path.dirname(os.path.realpath(__file__))+'/..'
		)
		self.rootUrl=data['rootUrl']
		self.pdfboxFilename=self.rootPath+'/bin/'+data['pdfboxJar']
		self.laws=(Law(self,lawData) for lawData in data['laws'])

e=Environment(data.data)
for law in e.laws:
	if not law.hasZip():
		raise Exception(law.zipFilename+' has to be downloaded')
	for document in law.documents:
		if not document.hasPdf():
			document.writePdf()
		if not document.hasTxt():
			document.writeTxt()
		if not document.hasCsvsAndXlss():
			document.writeCsvsAndXlss()