# basic types
# filenames are always absolute/ready to be read

import os.path
import io
import zipfile

import data

# приложения, которые парсим
class Document:
	def __init__(self,law,data):
		# path = путь внутри архива
		self.law=law
		self.pdfFilename=self.law.environment.rootPath+'/pdf/'+self.law.code+'.pdf'
		self.zipContents=data['zipContents']
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
		self.laws=(Law(self,lawData) for lawData in data['laws'])

e=Environment(data.data)
for law in e.laws:
	if not law.hasZip():
		raise Exception(law.zipFilename+' has to be downloaded')
	for document in law.documents:
		if not document.hasPdf():
			document.writePdf()
