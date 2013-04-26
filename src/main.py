# basic types
# filenames are always absolute/ready to be read
# paths are relative to root

import sys
import os.path
import io
import zipfile
import subprocess

import data,spreadsheet,writer

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
		sheet=spreadsheet.Spreadsheet(self.txtFilename,self.nCols)
		sheet.setDocumentTitle('Приложение '+str(self.appendixNumber)+' к Закону Санкт-Петербурга «'+self.law.title+'»')
		sheet.setTableTitle(self.title)
		sheet.setAmountHeader(header)
		for depth in range(1,4):
			sheet.build(depth,self.totals)
			for stairs in (False,True):
				for sums in (False,True):
					csvFilename=self.getCsvFilename(depth,stairs,sums)
					sheet.writeCsv(csvFilename,stairs,sums)
				xlsFilename=self.getXlsFilename(depth,stairs)
				sheet.writeXls(xlsFilename,self.delta,stairs)

# закон или законопроект, в к-рый входит несколько приложений - с ними отдельно разбираться
class Law:
	def __init__(self,environment,data):
		if 'documents' not in data:
			data['documents']=[]
		self.environment=environment
		self.code=data['code']
		self.year,version,pz=self.code.split('.')
		if version=='0':
			self.description='первоначальный'
		elif version in ('1','2','3'):
			self.description=version+'-я корректировка'
		elif version=='i':
			self.description='исполнение'
		else:
			raise Exception('unknown law version')
		if pz=='p':
			self.description+=' проект'
		elif pz=='z':
			self.description+=' закон'
		else:
			raise Exception('unknown law pz')
		self.viewUrl=data['viewUrl']
		self.downloadUrl=data['downloadUrl']
		if not self.downloadUrl.startswith(self.environment.rootUrl):
			raise Exception('invalid download url')
		self.title=data['title']
		self.documents=[Document(self,documentData) for documentData in data['documents']]
	@property
	def zipPath(self):
		return 'zip/'+self.downloadUrl[len(self.environment.rootUrl):]
	@property
	def zipFilename(self):
		return self.environment.rootPath+'/'+self.zipPath
	def hasZip(self):
		return os.path.isfile(self.zipFilename)

class Environment:
	def __init__(self,data):
		self.rootPath=os.path.realpath(
			os.path.dirname(os.path.realpath(__file__))+'/..'
		)
		self.rootUrl=data['rootUrl']
		self.pdfboxFilename=self.rootPath+'/bin/'+data['pdfboxJar']
		self.laws=[Law(self,lawData) for lawData in data['laws']]
		self.htmlFilename=self.rootPath+'/index.html'
	def hasHtml(self):
		return os.path.isfile(self.htmlFilename)
	def writeHtml(self):
		hw=writer.HtmlWriter(self)
		hw.write(self.htmlFilename)

env=Environment(data.data)
for law in env.laws:
	if not law.hasZip():
		raise Exception(law.zipFilename+' has to be downloaded')
	for document in law.documents:
		try:
			if not document.hasPdf():
				document.writePdf()
			if not document.hasTxt():
				document.writeTxt()
			if not document.hasCsvsAndXlss():
				document.writeCsvsAndXlss()
		except Exception as e:
			tb=sys.exc_info()[2]
			raise Exception(str(e)+' in document '+document.code).with_traceback(tb)
if not env.hasHtml():
	env.writeHtml()
