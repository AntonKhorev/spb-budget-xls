# laws data

# example codes:
# 2011.0.p
# 2011.0.z
# ^year
#      ^version = 0,1,2,...,i = исполнение
#        ^проект/закон

# Ведомственная структура расходов
#	в первой редакции - приложение 3
#	в изменениях - приложение 2 к изменению приложения 3

data={
	'rootUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/',
	'pdfboxJar':'pdfbox-app-1.8.1.jar',
	'laws':[
		# TODO 2010 and earlier
		{
			'code':'2011.0.p',
			'title':'О бюджете Санкт-Петербурга на 2011 год и на плановый период 2012 и 2013 годов',
			'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=413@cf_npa_bud',
			'downloadUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/2011/project/pr_2011-2013.zip',
			'documents':[
				{ # 06-окт-2010
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на 2011 год',
					'appendixNumber':3,
					'zipContents':'pr03_2011-2013.pdf',
					'forYear':2011,
					'total':'370 184 691,7',
				}
			],
		},{
			'code':'2011.0.z',
			'title':'О бюджете Санкт-Петербурга на 2011 год и на плановый период 2012 и 2013 годов',
			'date':'17.11.2010',
			'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=460@cf_npa_bud',
			'downloadUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/2011/full/bd2011-2013.zip',
			'documents':[
				{ # 23-ноя-2010
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на 2011 год',
					'appendixNumber':3,
					'zipContents':'pr03-bd11-13.pdf',
					'forYear':2011,
					'total':'380 714 669.6',
				}
			],
		},{
			'code':'2011.1.p',
			'title':'О внесении изменений в Закон Санкт-Петербурга “О бюджете Санкт-Петербурга на 2011 год и на плановый период 2012 и 2013 годов”',
			'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=476@cf_npa_bud',
			'downloadUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/2011/pr_1izm/pr-1izm2011.zip',
			'documents':[
				{ # 31-мар-2011
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на 2011 год',
					'appendixNumber':2,
					'zipContents':'pr02-2011-2013-pr-1izm.zip/pr02-2011-2013-pr-1izm.pdf',
					'forYear':2011,
					'total':'413 046 268.7',
				}
			],
		},{
			'code':'2011.1.z',
			'title':'О внесении изменений в Закон Санкт-Петербурга “О бюджете Санкт-Петербурга на 2011 год и на плановый период 2012 и 2013 годов” ',
			'date':'25.05.2011',
			'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=483@cf_npa_bud',
			'downloadUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/2011/1izm/bd_2011-13-1izm.zip',
			'documents':[
				{ # 01-июн-2011
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на 2011 год',
					'appendixNumber':2,
					'zipContents':'pr_02_2011-2013-1izm.pdf',
					'forYear':2011,
					'total':'431 939 763.4',
				}
			],
		},{
			'code':'2011.i.z',
			'title':'Об исполнении бюджета Санкт-Петербурга за 2011 год',
			'date':'27.06.2012',
			'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=555@cf_npa_bud',
			'downloadUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/2011/ispolnenie/isp2011.zip',
			# другого формата
			# 'documents':[
				# {
					# 'title':'Показатели расходов бюджета Санкт-Петербурга за 2011 год по ведомственной структуре расходов бюджета Санкт-Петербурга',
					# 'appendixNumber':4,
					# 'zipContents':'isp2011-pr4.pdf',
					# 'forYear':2011,
					# 'total':('431 939 763.4','442 067 920.3','404 032 373.1')
				# }
			# ],
		},{
			'code':'2012.0.p',
			'title':'О бюджете Санкт-Петербурга на 2012 год и на плановый период 2013 и 2014 годов',
			'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=503@cf_npa_bud',
			'downloadUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/2012/project/pr_2012-2014.zip',
			'documents':[
				{ # 12-сен-2011
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на 2012 год',
					'appendixNumber':3,
					'zipContents':'pr03_2012-2014.pdf',
					'forYear':2012,
					'total':'404 233 953.4',
				}
			],
		},{
			'code':'2012.0.z',
			'title':'О бюджете Санкт-Петербурга на 2012 год и на плановый период 2013 и 2014 годов',
			'date':'26.10.2011',
			'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=506@cf_npa_bud',
			'downloadUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/2012/full/bd2012-14.zip',
			'documents':[
				{ # 27-окт-2011
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на 2012 год',
					'appendixNumber':3,
					'zipContents':'pr03-2012.zip/pr03-2012.pdf',
					'forYear':2012,
					'total':'418 351 302.1',
				}
			],
		},{
			'code':'2012.1.p',
			'title':'О внесении изменений и дополнения в Закон Санкт-Петербурга «О бюджете Санкт-Петербурга на 2012 год и на плановый период 2013 и 2014 годов»',
			'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=533@cf_npa_bud',
			'downloadUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/2012/pr_1izm/pr_1izm_2012-14.zip',
			'documents':[
				{ # 28-мар-2012
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на 2012 год',
					'appendixNumber':2,
					'zipContents':'04_pr2-2012-14-pr1izm.zip/04_pr2-2012-14-pr1izm.pdf',
					'forYear':2012,
					'total':'430 425 000.8',
				}
			],
		},{
			'code':'2012.1.z',
			'title':'О внесении изменений и дополнений в Закон Санкт-Петербурга «О бюджете Санкт-Петербурга на 2012 год и на плановый период 2013 и 2014 годов»',
			'date':'23.05.2012',
			'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=542@cf_npa_bud',
			'downloadUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/2012/1izm/bd-12-14-1izm.zip',
			'documents':[
				{ # 31-май-2012
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на 2012 год',
					'appendixNumber':2,
					'zipContents':'pril_02-12-14-1izm.zip/pril_02-12-14-1izm.pdf',
					'forYear':2012,
					'total':'419 993 990.1',
				}
			],
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
			'title':'О бюджете Санкт-Петербурга на 2013 год и на плановый период 2014 и 2015 годов',
			'date':'28.11.2012',
			'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=586@cf_npa_bud',
			'downloadUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/2013/full/bd2013-15.zip',
			'documents':[
				{
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на 2013 год',
					'appendixNumber':3,
					'zipContents':'pr03_2013.pdf',
					'forYear':2013,
					'total':'411 033 787.5',
				}
			],
		},{
			'code':'2013.1.p',
			'title':'О внесении изменений и дополнений в Закон Санкт-Петербурга «О бюджете Санкт-Петербурга на 2013 год и на плановый период 2014 и 2015 годов»',
			'date':'12.04.2013',
			'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=602@cf_npa_bud',
			'downloadUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/2013/pr_1izm/pr_1izm.zip',
			'documents':[
				{
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на 2013 год',
					'appendixNumber':2,
					'zipContents':'pr02-1izm_2013-15.zip/pr02-1izm_2013-15.pdf',
					'forYear':2013,
					'total':'429 438 320.2',
				}
			],
		}
	],
}