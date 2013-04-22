# basic types
# filenames are always absolute/ready to be read

import os.path
import zipfile

import data

# приложения, которые парсим
class Document:
	def __init__(self,law,data):
		# path = путь внутри архива
		self.law=law
		self.pdfFilename=self.law.environment.rootPath+'/pdf/'+self.law.code+'.pdf'
		self.zipContents=data['zipContents']
	def writePdf(self):
		zipFile=zipfile.ZipFile(law.zipFilename)
		pdfFile=open(self.pdfFilename,'wb')
		pdfFile.write(
			zipFile.read(self.zipContents)
		)
		pdfFile.close()
		zipFile.close()

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
	def checkZip(self):
		if not os.path.isfile(self.zipFilename):
			raise Exception('file '+self.zipFilename+' not found')

class Environment:
	def __init__(self,data):
		self.rootPath=os.path.realpath(
			os.path.dirname(os.path.realpath(__file__))+'/..'
		)
		self.rootUrl=data['rootUrl']
		self.laws=(Law(self,lawData) for lawData in data['laws'])

e=Environment(data.data)
for law in e.laws:
	law.checkZip()
	for document in law.documents:
		document.writePdf()
