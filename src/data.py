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

# urlы можно без www писать
# title по шаблону не всегда можно сделать - есть небольшие различия

data={
	'rootUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/',
	'pdfboxJar':'pdfbox-app-1.8.1.jar',
	'laws':[
		# TODO 2008 and earlier
		{
			'code':'2009.0.p',
			'title':'О бюджете Санкт-Петербурга на 2009 год и на плановый период 2010 и 2011 годов',
			'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=286@cf_npa_bud',
			'downloadUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/2009/project/pr2009-2011.zip',
			'documents':[
				{ # 24-сен-08
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на 2009 год',
					'appendixNumber':3,
					'zipContents':'pr03_2009-2011.zip/pr03_2009-2011.pdf',
					'forYear':2009,
					'total':'423 001 779.4',
				},{
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на плановый период 2010 и 2011 годов',
					'appendixNumber':4,
					'zipContents':'pr04_2009-2011.zip/pr04_2009-2011.pdf',
					'forYear':(2010,2011),
					'total':('481 414 762.2','541 554 577.2'),
				}
			],
		},{
			'code':'2009.0.z',
			'title':'О бюджете Санкт-Петербурга на 2009 год и на плановый период 2010 и 2011 годов',
			'date':'19.11.2008',
			'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=290@cf_npa_bud',
			'downloadUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/2009/full/zakon2009.zip',
			'documents':[
				{ # 27-ноя-2008
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на 2009 год',
					'appendixNumber':3,
					'zipContents':'pr3_2009-2011.zip/pr3_2009-2011.pdf',
					'forYear':2009,
					'total':'397 178 072.2',
				},{
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на плановый период 2010 и 2011 годов',
					'appendixNumber':4,
					'zipContents':'pr4_2009-2011.zip/pr4_2009-2011.pdf',
					'forYear':(2010,2011),
					'total':('454 246 096.5','522 185 185.9'),
				}
			],
		},{
			# 'code':'2009.1.p',
			# 'title':'О внесении изменений в Закон Санкт-Петербурга «О бюджете Санкт-Петербурга на 2009 год и на плановый период 2010 и 2011 годов»',
			# 'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=293@cf_npa_bud',
			# 'dowloadUrl':'', # no download url...
		# },{
                	'code':'2009.1.z',
			'title':'О внесении изменений в Закон Санкт-Петербурга «О бюджете Санкт-Петербурга на 2009 год и на плановый период 2010 и 2011 годов»',
			'date':'01.04.2009',
			'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=296@cf_npa_bud',
			'downloadUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/2009/izm1/zakon-2009-2022-izm1.zip',
			'documents':[
				{ # 02-апр-2009
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на 2009 год',
					'appendixNumber':3,
					'zipContents':'pr3-2009-2011-1izm.zip/pr3-2009-2011-1izm.pdf',
					'forYear':2009,
					'total':'318 799 024.3',
				},{
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на плановый период 2010 и 2011 годов',
					'appendixNumber':4,
					'zipContents':'pr4-2009-2011-1izm.zip/pr4-2009-2011-1izm.pdf',
					'forYear':(2010,2011),
					'total':('364 369 187.6','430 894 568.1'),
				}
			],
		},{
                	'code':'2009.2.p',
			'title':'О внесении изменения в Закон Санкт-Петербурга «О бюджете Санкт-Петербурга на 2009 год и на плановый период 2010 и 2011 годов»',
			'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=300@cf_npa_bud',
			'downloadUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/2009/pr_izm2/zakon2009-2011-pr_izm2.pdf',
			# в проекте нет изменений данных, а в законе - уже есть
		},{
			# 'code':'2009.2.z',
			# 'title':'О внесении изменений в Закон Санкт-Петербурга «О бюджете Санкт-Петербурга на 2009 год и на плановый период 2010 и 2011 годов»',
			# 'date':'24.06.2009',
			# 'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=302@cf_npa_bud',
			# 'downloadUrl':'', # no download url
		# },{
			# 'code':'2009.3.p',
			# 'title':'О внесении изменения в Закон Санкт-Петербурга «О бюджете Санкт-Петербурга на 2009 год и на плановый период 2010 и 2011 годов»',
			# 'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=307@cf_npa_bud',
			# 'downloadUrl':'', # no download url
		# },{
			# 'code':'2009.3.z',
			# 'title':'О внесении изменений в Закон Санкт-Петербурга «О бюджете Санкт-Петербурга на 2009 год и на плановый период 2010 и 2011 годов»',
			# 'date':'28.10.2009',
			# 'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=327@cf_npa_bud',
			# 'downloadUrl':'', # no download url
		# },{
                	# 'code':'2009.i.z',
			# 'title':'Об исполнении бюджета Санкт-Петербурга за 2009 год',
			# 'date':'23.06.2010',
			# 'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=382@cf_npa_bud',
			# 'downloadUrl':'', # no download url
		# },{
			'code':'2010.0.p',
			'title':'О бюджете Санкт-Петербурга на 2010 год и на плановый период 2011 и 2012 годов',
			'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=308@cf_npa_bud',
			'downloadUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/2010/project/pr2010-2012.zip',
			'documents':[
				{ # 12-окт-2009
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на 2010 год',
					'appendixNumber':3,
					'zipContents':'pr03_2010-2012.pdf',
					'forYear':2010,
					'total':'324 279 318.4',
				},{
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на плановый период 2011 и 2012 годов',
					'appendixNumber':4,
					'zipContents':'pr04_2010-2012.pdf',
					'forYear':(2011,2012),
					'total':('343 194 788.3','380 631 227.2'),
				}
			],
		},{
			'code':'2010.0.z',
			'title':'О бюджете Санкт-Петербурга на 2010 год и на плановый период 2011 и 2012 годов',
			'date':'25.11.2009',
			'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=332@cf_npa_bud',
			'downloadUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/2010/full/bd_spb_2010-12.zip',
			'documents':[
				{ # 02-дек-2009
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на 2010 год',
					'appendixNumber':3,
					'zipContents':'pr3_2010-2012.zip/pr3_2010-2012.pdf',
					'forYear':2010,
					'total':'336 701 583.2',
				},{
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на плановый период 2011 и 2012 годов',
					'appendixNumber':4,
					'zipContents':'pr4_2010-2012.zip/pr4_2010-2012.pdf',
					'forYear':(2011,2012),
					'total':('341 359 895.7','371 160 398.8'),
				}
			],
		},{
			'code':'2010.1.p',
			'title':'О внесении изменений в Закон Санкт-Петербурга «О бюджете Санкт-Петербурга на 2010 год и на плановый период 2011 и 2012 годов»',
			'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=372@cf_npa_bud',
			'downloadUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/2010/pr_izm1/pr_izm1.zip',
			'documents':[
				{ # 09-апр-2010
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на 2010 год',
					'appendixNumber':3,
					'zipContents':'pr03-2010-12-pr_izm1.zip/pr03-2010-12-pr_izm1.pdf',
					'forYear':2010,
					'total':'355 707 925,7',
				},{
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на плановый период 2011 и 2012 годов',
					'appendixNumber':4,
					'zipContents':'pr04-2010-12-pr_izm1.zip/pr04-2010-12-pr_izm1.pdf',
					'forYear':(2011,2012),
					'total':('341 152 263,9','370 932 954,9'),
				}
			],
		},{
			'code':'2010.1.z',
			'title':'О внесении изменений в Закон Санкт-Петербурга «О бюджете Санкт-Петербурга на 2010 год и на плановый период 2011 и 2012 годов»',
			'date':'26.05.2010',
			'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=378@cf_npa_bud',
			'downloadUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/2010/1izm/zakon_pr-2010-2012-1izm.zip',
			'documents':[
				{ # 04-июн-2010
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на 2010 год',
					'appendixNumber':3,
					'zipContents':'pr3-2010-2012-1izm.zip/pr3-2010-2012-1izm.pdf',
					'forYear':2010,
					'total':'378 816 206.7',
				},{
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на плановый период 2011 и 2012 годов',
					'appendixNumber':4,
					'zipContents':'pr4-2010-2012-1izm.zip/pr4-2010-2012-1izm.pdf',
					'forYear':(2011,2012),
					'total':('341 152 263.9','370 932 954.9'),
				}
			],
		},{
			'code':'2010.i.z',
			'title':'Об исполнении бюджета Санкт-Петербурга за 2010 год',
			'date':'29.06.2011',
			'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=498@cf_npa_bud',
			'downloadUrl':[
				'http://www.fincom.spb.ru/files/cf/npd/budget/2010/ispolnenie/isp2010-pril1-1.pdf',
				'http://www.fincom.spb.ru/files/cf/npd/budget/2010/ispolnenie/isp2010-pril1-2.zip',
				'http://www.fincom.spb.ru/files/cf/npd/budget/2010/ispolnenie/isp2010-pril1-3.pdf',
				'http://www.fincom.spb.ru/files/cf/npd/budget/2010/ispolnenie/isp2010-pril2.pdf',
				'http://www.fincom.spb.ru/files/cf/npd/budget/2010/ispolnenie/isp2010-pril3.pdf',
				'http://www.fincom.spb.ru/files/cf/npd/budget/2010/ispolnenie/isp2010-pril4.zip',
				'http://www.fincom.spb.ru/files/cf/npd/budget/2010/ispolnenie/isp2010-pril5.pdf',
				'http://www.fincom.spb.ru/files/cf/npd/budget/2010/ispolnenie/isp2010-pril6.pdf',
				'http://www.fincom.spb.ru/files/cf/npd/budget/2010/ispolnenie/isp2010-pril7.pdf',
			],
			'documents':[
				{
					'title':'Показатели расходов бюджета Санкт-Петербурга за 2010 год по ведомственной структуре расходов бюджета Санкт-Петербурга',
					'appendixNumber':4,
					'zipFilename':'2010/ispolnenie/isp2010-pril4.zip',
					'zipContents':'isp2010-pril4.pdf',
					'forYear':2010,
					'total':('378 816 206.7','386 042 260.7','358 567 281.7'),
				}
			],
		},{
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
				},{
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на плановый период 2012 и 2013 годов',
					'appendixNumber':4,
					'zipContents':'pr04_2011-2013.pdf',
					'forYear':(2012,2013),
					'total':('382 893 401,8','414 684 681,6'),
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
				},{
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на плановый период 2012 и 2013 годов',
					'appendixNumber':4,
					'zipContents':'pr04-bd11-13.pdf',
					'forYear':(2012,2013),
					'total':('382 889 891.4','414 681 120.2'),
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
				},{
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на плановый период 2012 и 2013 годов',
					'appendixNumber':9,
					'zipContents':'pr09-2012-2013-pr-1izm.pdf',
					'forYear':(2012,2013),
					'total':('+5 889 897.5','+0.0'),
					'delta':True,
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
				},{
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на плановый период 2012 и 2013 годов',
					'appendixNumber':10,
					'zipContents':'pr_10_2011-2013-1izm.pdf',
					'forYear':(2012,2013),
					'total':('+5 889 897.5','+0.0'),
					'delta':True,
				}
			],
		},{
			'code':'2011.i.z',
			'title':'Об исполнении бюджета Санкт-Петербурга за 2011 год',
			'date':'27.06.2012',
			'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=555@cf_npa_bud',
			'downloadUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/2011/ispolnenie/isp2011.zip',
			'documents':[
				{
					'title':'Показатели расходов бюджета Санкт-Петербурга за 2011 год по ведомственной структуре расходов бюджета Санкт-Петербурга',
					'appendixNumber':4,
					'zipContents':'isp2011-pr4.pdf',
					'forYear':2011,
					'total':('431 939 763.4','442 067 920.3','404 032 373.1'),
				}
			],
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
				},{
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на плановый период 2013 и 2014 годов',
					'appendixNumber':4,
					'zipContents':'pr04_2012-2014.pdf',
					'forYear':(2013,2014),
					'total':('403 282 608.1','441 718 227.4'),
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
				},{
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на плановый период 2013 и 2014 годов',
					'appendixNumber':4,
					'zipContents':'pr04-2013-2014.zip/pr04-2013-2014.pdf',
					'forYear':(2013,2014),
					'total':('428 553 231.6','469 472 031.2'),
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
				},{
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на плановый период 2013 и 2014 годов',
					'appendixNumber':7,
					'zipContents':'09_pr7-2012-14-pr1izm.pdf',
					'forYear':(2013,2014),
					'total':('162 951.0','50 000.0'),
					'delta':True,
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
				},{
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на плановый период 2013 и 2014 годов',
					'appendixNumber':9,
					'zipContents':'pril_09-12-14-1izm.pdf',
					'forYear':(2013,2014),
					'total':('+0.0','+0.0'),
					'delta':True,
					# 'missingEntries':['26.1.','26.2.','26.6.','29.7.','31.1.','31.3.'], # просто ряд пропущен - видимо потому, что в сумме 0
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
				},{
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на плановый период 2014 и 2015 годов',
					'appendixNumber':4,
					'zipContents':'pr04-2013-15.pdf',
					'forYear':(2014,2015),
					'total':('435 351 616.5','464 599 092.2'),
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
				},{
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на плановый период 2014 и 2015 годов',
					'appendixNumber':4,
					'zipContents':'pr04_2014-2015.pdf',
					'forYear':(2014,2015),
					'total':('435 351 616.5','464 599 092.2'),
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
				},{
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на плановый период 2014 и 2015 годов',
					'appendixNumber':8,
					'zipContents':'pr08-1izm_2013-15.pdf',
					'forYear':(2014,2015),
					'total':('-869 518.5','-973 581.1'),
					'delta':True, # в формате +/-
				}
			],
		},{
			'code':'2013.1.z',
			'title':'О внесении изменений и дополнений в Закон Санкт-Петербурга «О бюджете Санкт-Петербурга на 2013 год и на плановый период 2014 и 2015 годов»',
			'date':'22.05.2013',
			'viewUrl':'http://www.fincom.spb.ru/comfin/budjet/laws/doc.htm?id=613@cf_npa_bud',
			'downloadUrl':'http://www.fincom.spb.ru/files/cf/npd/budget/2013/1izm/1izm-bd-2013-15.zip',
			'documents':[
				{
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на 2013 год',
					'appendixNumber':2,
					'zipContents':'pr02-1izm-2013-15.zip/pr02-1izm-2013-15.pdf',
					'forYear':2013,
					'total':'426 643 042.8',
				},{
					'title':'Ведомственная структура расходов бюджета Санкт-Петербурга на плановый период 2014 и 2015 годов',
					'appendixNumber':9,
					'zipContents':'pr09-1izm-2013-15.pdf',
					'forYear':(2014,2015),
					'total':('-2 969 518.5','-973 581.1'),
					'delta':True, # в формате +/-
				}
			],
		}
	],
}
