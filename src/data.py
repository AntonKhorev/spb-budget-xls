# laws data

# example codes:
# 2011.0.p
# 2011.0.z
# ^year
#      ^version = 0,1,2,...,i = исполнение
#        ^проект/закон

data={
	'rootUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/',
	'laws':[
		# TODO 2010 and earlier
		{
			'code':'2011.0.p',
			'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=413@cf_npa_bud',
			'downloadUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/2011/project/pr_2011-2013.zip'
		},{
			'code':'2011.0.z',
			'date':'17.11.2010',
			'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=460@cf_npa_bud',
			'downloadUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/2011/full/bd2011-2013.zip',
		},{
			'code':'2011.1.p',
			'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=476@cf_npa_bud',
			'downloadUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/2011/pr_1izm/pr-1izm2011.zip',
		},{
			'code':'2011.1.z',
			'date':'25.05.2011',
			'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=483@cf_npa_bud',
			'downloadUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/2011/1izm/bd_2011-13-1izm.zip',
		},{
			'code':'2011.i.p',
			'date':'27.06.2012',
			'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=555@cf_npa_bud',
			'downloadUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/2011/ispolnenie/isp2011.zip',
		},{
			'code':'2012.0.p',
			'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=503@cf_npa_bud',
			'downloadUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/2012/project/pr_2012-2014.zip',
		},{
			'code':'2012.0.z',
			'date':'26.10.2011',
			'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=506@cf_npa_bud',
			'downloadUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/2012/full/bd2012-14.zip',
		},{
			'code':'2012.1.p',
			'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=533@cf_npa_bud',
			'downloadUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/2012/pr_1izm/pr_1izm_2012-14.zip',
		},{
			'code':'2012.1.z',
			'date':'23.05.2012',
			'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=542@cf_npa_bud',
			'downloadUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/2012/1izm/bd-12-14-1izm.zip',
		},{
			'code':'2013.0.p',
			'title':'О бюджете Санкт-Петербурга на 2013 год и на плановый период 2014 и 2015 годов',
			'date':'02.10.2012',
			'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=569@cf_npa_bud',
			'downloadUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/2013/project/pr-bd-2013-15.zip',
			'documents':[
				{
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на 2013 год',
					'appendixNumber':3,
					'zipContents':'pr03-2013-15.pdf',
					'forYear':2013,
					'total':'405 880 212.3',
				}
			],
		},{
			'code':'2013.0.z',
			'date':'28.11.2012',
			'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=586@cf_npa_bud',
			'downloadUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/2013/full/bd2013-15.zip',
		},{
			'code':'2013.1.p',
			'date':'12.04.2013',
			'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=602@cf_npa_bud',
			'downloadUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/2013/pr_1izm/pr_1izm.zip',
		}
	],
}
