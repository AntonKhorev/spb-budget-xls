# bill data

import os.path

import data

# приложения, которые парсим
class Document:
	def __init__(self,**kwargs):
		# path = путь внутри архива
		pass

# закон или законопроект, в к-рый входит несколько приложений - с ними отдельно разбираться
class Law:
	def __init__(self,environment,data):
		# year = на какой год (первый из (трёх) годов)
		# date = дата опубликования
		# viewUrl = url для просмотра
		# downloadUrl = url для скачивания
		#	из него будет делаться путь к скачанным файлам в /zip
		#	http://www.fincom.spb.ru/files/cf/npd/budget/ - всё, что после = путь
		# version =
		#	0 - исходный закон/проект
		#	1,2,3,... - n-я корректировка (пока была только одна корректировка, даты есть только для 2013)
		#		бывает и больше корректировок
		#	-1 - закон об исполнении (его проекта нет, в зипе только приложения)
		self.environment=environment
		if not data['downloadUrl'].startswith(self.environment.rootUrl):
			raise Exception('invalid download url')
		self.zipFilename=data['downloadUrl'][len(self.environment.rootUrl):]
	def checkZip(self):
		filename=self.environment.rootPath+'/zip/'+self.zipFilename
		if not os.path.isfile(filename):
			raise Exception('file '+filename+' not found')

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
