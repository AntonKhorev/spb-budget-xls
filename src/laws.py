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
	def getCsvAttrs(self):
		for sums in (False,True):
			for depth in range(1,4):
				filename=self.law.environment.rootPath+'/csv/'+self.code+'('+str(depth)+(',sums' if sums else '')+').csv'
				yield sums,depth,filename
	def hasCsvs(self):
		for _,_,csvFilename in self.getCsvAttrs():
			if not os.path.isfile(csvFilename):
				return False
		return True
	def writeCsvs(self):
		for sums,depth,csvFilename in self.getCsvAttrs():
			spreadsheet=parse.Spreadsheet(depth,sums)
			spreadsheet.read(self.txtFilename,self.nCols)
			spreadsheet.checkTotals(self.totals)
			# TODO add column headers
			# example for pr04-2013-15.txt:
			# spreadsheet.setAmountHeader({0:'Плановый период 2014 г. (тыс. руб.)',1:'Плановый период 2015 г. (тыс. руб.)'})
			# TODO add document name somewhere
			spreadsheet.write(csvFilename)

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
		if not document.hasCsvs():
			document.writeCsvs()
