# bill data

import os.path
import urllib.parse

# закон или законопроект, в к-рый входит несколько приложений - с ними отдельно разбираться
class Law:
	def __init__(self,**kwargs):
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
		url=urllib.parse.urlparse(kwargs['downloadUrl'])
		prefix='/files/cf/npd/budget/'
		if not url.path.startswith(prefix):
			raise Exception('invalid download url')
		self.filename=url.path[len(prefix):]
	def checkFile(self):
		root=os.path.realpath(
			os.path.dirname(os.path.realpath(__file__))+'/..'
		)
		filename=root+'/zip/'+self.filename
		if not os.path.isfile(filename):
			raise Exception('file '+filename+' not found')

# проект
class Bill(Law):
	pass

# закон (д.б. с номером, а то они иногда проект обозначают как закон)
class Act(Law):
	pass

laws=[
	# TODO 2010 and earlier
	Bill(
		year=2011,
		viewUrl='http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=413@cf_npa_bud',
		downloadUrl='http://www.fincom.spb.ru/files/cf/npd/budget/2011/project/pr_2011-2013.zip',
		version=0
	),
	Act(
		year=2011,
		date='17.11.2010',
		viewUrl='http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=460@cf_npa_bud',
		downloadUrl='http://www.fincom.spb.ru/files/cf/npd/budget/2011/full/bd2011-2013.zip',
		version=0
	),
	Bill(
		year=2011,
		viewUrl='http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=476@cf_npa_bud',
		downloadUrl='http://www.fincom.spb.ru/files/cf/npd/budget/2011/pr_1izm/pr-1izm2011.zip',
		version=1
	),
	Act(
		year=2011,
		date='25.05.2011',
		viewUrl='http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=483@cf_npa_bud',
		downloadUrl='http://www.fincom.spb.ru/files/cf/npd/budget/2011/1izm/bd_2011-13-1izm.zip',
		version=1
	),
	Act(
		year=2011,
		date='27.06.2012',
		viewUrl='http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=555@cf_npa_bud',
		downloadUrl='http://www.fincom.spb.ru/files/cf/npd/budget/2011/ispolnenie/isp2011.zip',
		version=-1
	),
	Bill(
		year=2012,
		viewUrl='http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=503@cf_npa_bud',
		downloadUrl='http://www.fincom.spb.ru/files/cf/npd/budget/2012/project/pr_2012-2014.zip',
		version=0
	),
	Act(
		year=2012,
		date='26.10.2011',
		viewUrl='http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=506@cf_npa_bud',
		downloadUrl='http://www.fincom.spb.ru/files/cf/npd/budget/2012/full/bd2012-14.zip',
		version=0
	),
	Bill(
		year=2012,
		viewUrl='http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=533@cf_npa_bud',
		downloadUrl='http://www.fincom.spb.ru/files/cf/npd/budget/2012/pr_1izm/pr_1izm_2012-14.zip',
		version=1
	),
	Act(
		year=2012,
		date='23.05.2012',
		viewUrl='http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=542@cf_npa_bud',
		downloadUrl='http://www.fincom.spb.ru/files/cf/npd/budget/2012/1izm/bd-12-14-1izm.zip',
		version=1
	),
	Bill(
		year=2013,
		date='02.10.2012',
		viewUrl='http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=569@cf_npa_bud',
		downloadUrl='http://www.fincom.spb.ru/files/cf/npd/budget/2013/project/pr-bd-2013-15.zip',
		version=0
	),
	Act(
		year=2013,
		date='28.11.2012',
		viewUrl='http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=586@cf_npa_bud',
		downloadUrl='http://www.fincom.spb.ru/files/cf/npd/budget/2013/full/bd2013-15.zip',
		version=0
	),
	Bill(
		year=2013,
		date='12.04.2013',
		viewUrl='http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=602@cf_npa_bud',
		downloadUrl='http://www.fincom.spb.ru/files/cf/npd/budget/2013/pr_1izm/pr_1izm.zip',
		version=1
	),
]

for law in laws:
	law.checkFile()
