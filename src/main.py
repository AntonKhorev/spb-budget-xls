#!/usr/bin/env python3

# basic types
# filenames are always absolute/ready to be read
# paths are relative to root

import sys
import os.path
import io,shutil,zipfile
import subprocess
import urllib.request
import yaml

import spreadsheet,xlsWriter

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
		if 'pdfFilename' in data:
			self.downloadedPdfFilename=self.law.environment.rootPath+'/zip/'+data['pdfFilename']
		else:
			if 'zipFilename' in data:
				self.zipFilename=self.law.environment.rootPath+'/zip/'+data['zipFilename']
			else:
				self.zipFilename=law.zipFilename
			self.zipContents=data['zipContents']
		self.pdfFilename=self.law.environment.rootPath+'/pdf/'+self.code+'.pdf'
		self.txtFilename=self.law.environment.rootPath+'/txt/'+self.code+'.txt'
		self.totals=data['total']
		if self.law.version=='i':
			if len(self.forYears)!=1 or len(self.totals)!=3:
				raise Exception('invalid number of columns')
		else:
			if len(self.forYears)!=len(self.totals):
				raise Exception('invalid number of columns')
		self.nCols=len(self.totals)
		self.delta=data['delta']
		self.appendixNumber=data['appendixNumber']
		self.title=data['title']
		if 'quirks' in data:
			self.quirks=set(data['quirks'])
		else:
			self.quirks=set()
	@property
	def maxDepth(self):
		return 4 if 'depth4' in self.quirks else 3
	def hasPdf(self):
		return os.path.isfile(self.pdfFilename)
	def writePdf(self):
		# just copy the file if it's not zipped
		if hasattr(self,'downloadedPdfFilename'):
			shutil.copyfile(self.downloadedPdfFilename,self.pdfFilename)
			return
		# attempt to read before opening pdfFile - otherwise might get zero-length file on error
		bytes=None
		for s in self.zipContents.split('/'):
			if bytes is None:
				zipFile=zipfile.ZipFile(self.zipFilename)
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
	def getCsvPath(self,depth,stairs,sums):
		return 'csv/'+self.code+self.getFilenameParensPart(depth,stairs,sums)+'.csv'
	def getCsvFilename(self,depth,stairs,sums):
		return self.law.environment.rootPath+'/'+self.getCsvPath(depth,stairs,sums)
	def getXlsPath(self,depth,stairs):
		sums=True
		return 'xls/'+self.code+self.getFilenameParensPart(depth,stairs,sums)+'.xls'
	def getXlsFilename(self,depth,stairs):
		return self.law.environment.rootPath+'/'+self.getXlsPath(depth,stairs)
	def hasCsvsAndXlss(self):
		for depth in range(1,self.maxDepth+1):
			for stairs in (False,True):
				for sums in (False,True):
					if not os.path.isfile(self.getCsvFilename(depth,stairs,sums)):
						return False
				if not os.path.isfile(self.getXlsFilename(depth,stairs)):
					return False
		return True
	def writeCsvsAndXlss(self):
		if self.law.version=='i':
			sheet=spreadsheet.Spreadsheet(self.txtFilename,self.nCols,nPercentageCols=2,quirks=self.quirks)
			sheet.setAmountHeader(['Утверждено по бюджету (тыс. руб.)','План с учетом изменений на отчетный период (тыс. руб.)','Исполнено с начала года (тыс. руб.)'])
			sheet.setSlackHeader({self.nCols-1:'Поправка на округление (тыс. руб.)'})
		else:
			sheet=spreadsheet.Spreadsheet(self.txtFilename,self.nCols,quirks=self.quirks)
			sheet.setAmountHeader([('Изменение суммы' if self.delta else 'Сумма')+' на '+year+' г. (тыс. руб.)' for year in self.forYears])
			if 'slack' in self.quirks:
				sheet.setSlackHeader({k:'Расхождение (тыс. руб.)' for k in range(self.nCols)})
		sheet.setDocumentTitle('Приложение '+str(self.appendixNumber)+' к Закону Санкт-Петербурга «'+self.law.title+'»')
		sheet.setTableTitle(self.title)
		for depth in range(1,self.maxDepth+1):
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
		if isinstance(data['downloadUrl'],str):
			data['downloadUrl']=[data['downloadUrl']]
		self.environment=environment
		self.code=data['code']
		self.year,self.version,pz=self.code.split('.')
		if self.version=='0':
			self.description='первоначальный'
			if 'title' not in data: # not reliable
				data['title']='О бюджете Санкт-Петербурга на '+self.year+' год и на плановый период '+str(int(self.year)+1)+' и '+str(int(self.year)+2)+' годов'
		elif self.version in ('1','2','3'):
			self.description=self.version+'-я корректировка'
		elif self.version=='i':
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
		self.downloadUrls=data['downloadUrl']
		self.originalXlsUrl=data.get('originalXlsUrl')
		if self.originalXlsUrl==True:
			self.originalXlsUrl=self.downloadUrls[0]
		for du in self.downloadUrls:
			if not du.startswith(self.environment.rootUrl):
				raise Exception('invalid download url '+du)
		self.title=data['title']
		self.documents=[Document(self,documentData) for documentData in data['documents']]
		if 'availabilityNote' in data:
			self.availabilityNote=data['availabilityNote']
		elif self.originalXlsUrl is not None:
			self.availabilityNote="данные доступны на сайте Комитета финансов в формате xls"
		elif not self.documents:
			self.availabilityNote="не содержит ведомственной структуры расходов"
		else:
			self.availabilityNote=None
	@property
	def isSingleDownload(self):
		return len(self.downloadUrls)==1
	@property
	def isSingleZip(self):
		return self.isSingleDownload and self.downloadUrls[0][-4:]=='.zip'
	@property
	def downloadUrl(self):
		if not self.isSingleDownload:
			raise Exception('law has no single download url')
		return self.downloadUrls[0]
	@property
	def zipPath(self):
		if not self.isSingleZip:
			raise Exception('law has no single zip')
		return 'zip/'+self.downloadUrl[len(self.environment.rootUrl):]
	@property
	def filePaths(self):
		return ('zip/'+du[len(self.environment.rootUrl):] for du in self.downloadUrls)
	@property
	def zipFilename(self):
		if not self.isSingleZip:
			raise Exception('law has no single zip')
		return self.environment.rootPath+'/'+self.zipPath
	@property
	def filenames(self):
		return (self.environment.rootPath+'/'+fp for fp in self.filePaths)
	def hasFiles(self):
		return all(os.path.isfile(filename) for filename in self.filenames)
	def downloadFiles(self):
		for filename,downloadUrl in zip(self.filenames,self.downloadUrls):
			os.makedirs(os.path.dirname(filename),exist_ok=True)
			print('downloading',downloadUrl)
			with urllib.request.urlopen(downloadUrl) as dl, open(filename,'wb') as file:
				file.write(dl.read())

class Environment:
	def __init__(self,data):
		self.rootPath=os.path.realpath(
			os.path.dirname(os.path.realpath(__file__))+'/..'
		)
		self.rootUrl=data['rootUrl']
		self.pdfboxFilename=self.rootPath+'/bin/'+data['pdfboxJar']
		self.laws=[Law(self,lawData) for lawData in data['laws']]
		self.htmlFilename=self.rootPath+'/xls.html'
	def hasHtml(self):
		return os.path.isfile(self.htmlFilename)
	def writeHtml(self,linker=None):
		hw=xlsWriter.XlsHtmlWriter(linker,self)
		hw.write(self.htmlFilename)

def loadData():
	return yaml.load(open(
		os.path.dirname(os.path.realpath(__file__))+'/data.yml',
		encoding='utf-8'
	))

if __name__=='__main__':
	env=Environment(loadData())
	for law in env.laws:
		if not law.hasFiles():
			law.downloadFiles()
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
