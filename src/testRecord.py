#!/usr/bin/env python3

import unittest

import record

class TestRecordBuilder(unittest.TestCase):
	def setUp(self):
		self.text1=[
			"1. АДМИНИСТРАЦИЯ ГУБЕРНАТОРА САНКТ- 2 114 774,1",
			"ПЕТЕРБУРГА (801)",
			"1.1. Расходы на содержание главы Правительства 0102 0010008 2 026,0",
			"Санкт-Петербурга",
			"1.1.1. Выполнение функций государственными органами 0102 0010008 012 2 026,0",
			"1.2. Содержание исполнительного органа 0114 0010009 984 695,5",
		]
		self.lr1=record.RecordBuilder(1)
		self.lr2=record.RecordBuilder(2)

	def doTestName(self,lr,lines,name):
		rows=[None]
		for i in range(len(lines)-1):
			lines[i+1]=lr.read(rows,lines[i],lines[i+1])
		self.assertEqual(rows[-1]['name'],name)

	def test1(self):
		rows=[None]
		nextLine=self.lr1.read(rows,self.text1[0],self.text1[1])
		self.assertEqual(nextLine,self.text1[1])
		self.assertEqual(rows,[None,
			{'number':'1.','name':'АДМИНИСТРАЦИЯ ГУБЕРНАТОРА САНКТ-','amounts':[21147741]},
		])
	def test1next(self):
		rows=[None,
			{'number':'1.','name':'АДМИНИСТРАЦИЯ ГУБЕРНАТОРА САНКТ-','amounts':[21147741]},
		]
		nextLine=self.lr1.read(rows,self.text1[1],self.text1[2])
		self.assertEqual(nextLine,self.text1[2])
		self.assertEqual(rows,[None,
			{'number':'1.','name':'АДМИНИСТРАЦИЯ ГУБЕРНАТОРА САНКТ-ПЕТЕРБУРГА (801)','amounts':[21147741]},
		])
	def test11(self):
		rows=[None,
			{'number':'1.','name':'АДМИНИСТРАЦИЯ ГУБЕРНАТОРА САНКТ-ПЕТЕРБУРГА (801)','amounts':[21147741]},
		]
		nextLine=self.lr1.read(rows,self.text1[2],self.text1[3])
		self.assertEqual(nextLine,self.text1[3])
		self.assertEqual(rows,[None,
			{'number':'1.','name':'АДМИНИСТРАЦИЯ ГУБЕРНАТОРА САНКТ-ПЕТЕРБУРГА (801)','amounts':[21147741]},
			{'number':'1.1.','name':'Расходы на содержание главы Правительства','section':'0102','article':'0010008','amounts':[20260]},
		])
	def test11next(self):
		rows=[None,
			{'number':'1.','name':'АДМИНИСТРАЦИЯ ГУБЕРНАТОРА САНКТ-ПЕТЕРБУРГА (801)','amounts':[21147741]},
			{'number':'1.1.','name':'Расходы на содержание главы Правительства','section':'0102','article':'0010008','amounts':[20260]},
		]
		nextLine=self.lr1.read(rows,self.text1[3],self.text1[4])
		self.assertEqual(nextLine,self.text1[4])
		self.assertEqual(rows,[None,
			{'number':'1.','name':'АДМИНИСТРАЦИЯ ГУБЕРНАТОРА САНКТ-ПЕТЕРБУРГА (801)','amounts':[21147741]},
			{'number':'1.1.','name':'Расходы на содержание главы Правительства Санкт-Петербурга','section':'0102','article':'0010008','amounts':[20260]},
		])
	def test111(self):
		rows=[None,
			{'number':'1.','name':'АДМИНИСТРАЦИЯ ГУБЕРНАТОРА САНКТ-ПЕТЕРБУРГА (801)','amounts':[21147741]},
			{'number':'1.1.','name':'Расходы на содержание главы Правительства Санкт-Петербурга','section':'0102','article':'0010008','amounts':[20260]},
		]
		nextLine=self.lr1.read(rows,self.text1[4],self.text1[5])
		self.assertEqual(nextLine,self.text1[5])
		self.assertEqual(rows,[None,
			{'number':'1.','name':'АДМИНИСТРАЦИЯ ГУБЕРНАТОРА САНКТ-ПЕТЕРБУРГА (801)','amounts':[21147741]},
			{'number':'1.1.','name':'Расходы на содержание главы Правительства Санкт-Петербурга','section':'0102','article':'0010008','amounts':[20260]},
			{'number':'1.1.1.','name':'Выполнение функций государственными органами','section':'0102','article':'0010008','type':'012','amounts':[20260]},
		])
	def testNumberPartOnNextLine(self):
		rows=[None]
		nextLine=self.lr2.read(rows,
			'12.12. Выполнение функций государственными 0707 4320024 012 -668 622.3 -670 998.3',
			'1. органами'
		)
		self.assertEqual(nextLine,'органами')
		self.assertEqual(rows,[None,
			{'number':'12.12.1.','name':'Выполнение функций государственными','section':'0707','article':'4320024','type':'012','amounts':[-6686223,-6709983]}
		])
	def testSpacesAroundQuote(self):
		rows=[None]
		line='63.18. Расходы на выполнение мероприятий по 0501 3500910 808.0'
		nextLine='обследованию и сносу " деревьев-угроз" , '
		line=self.lr1.read(rows,line,nextLine)
		self.assertEqual(line,nextLine)
		self.assertEqual(rows,[None,
			{'number':'63.18.','name':'Расходы на выполнение мероприятий по','section':'0501','article':'3500910','amounts':[8080]},
		])
		nextLine='находящихся на придомовой территории, не '
		line=self.lr1.read(rows,line,nextLine)
		self.assertEqual(line,nextLine)
		self.assertEqual(rows,[None,
			{'number':'63.18.','name':'Расходы на выполнение мероприятий по обследованию и сносу "деревьев-угроз",','section':'0501','article':'3500910','amounts':[8080]},
		])
	def testDoubleSpace(self):
		rows=[None]
		line="1.3. Расходы на материальное обеспечение 0103 0011201 149.0"
		nextLine="деятельности  членов Совета Федерации и их "
		line=self.lr1.read(rows,line,nextLine)
		self.assertEqual(line,nextLine)
		self.assertEqual(rows,[None,
			{'number':'1.3.','name':'Расходы на материальное обеспечение','section':'0103','article':'0011201','amounts':[1490]},
		])
		nextLine="помощников за счет средств федерального "
		line=self.lr1.read(rows,line,nextLine)
		self.assertEqual(line,nextLine)
		self.assertEqual(rows,[None,
			{'number':'1.3.','name':'Расходы на материальное обеспечение деятельности членов Совета Федерации и их','section':'0103','article':'0011201','amounts':[1490]},
		])
	def testPrirodopolzovanie(self):
		rows=[None]
		line='24. КОМИТЕТ ПО 1 963 666.1 1 467 692.3'
		nextLine='ПРИРОДОПОЛЬЗОВАНИЮ, ОХРАНЕ '
		line=self.lr2.read(rows,line,nextLine)
		self.assertEqual(line,nextLine)
		self.assertEqual(rows,[None,
			{'number':'24.','name':'КОМИТЕТ ПО','amounts':[19636661,14676923]},
		])
		nextLine='ОКРУЖАЮЩЕЙ СРЕДЫ И '
		line=self.lr2.read(rows,line,nextLine)
		self.assertEqual(line,nextLine)
		self.assertEqual(rows,[None,
			{'number':'24.','name':'КОМИТЕТ ПО ПРИРОДОПОЛЬЗОВАНИЮ, ОХРАНЕ','amounts':[19636661,14676923]},
		])
		nextLine='ОБЕСПЕЧЕНИЮ ЭКОЛОГИЧЕСКОЙ '
		line=self.lr2.read(rows,line,nextLine)
		self.assertEqual(line,nextLine)
		self.assertEqual(rows,[None,
			{'number':'24.','name':'КОМИТЕТ ПО ПРИРОДОПОЛЬЗОВАНИЮ, ОХРАНЕ ОКРУЖАЮЩЕЙ СРЕДЫ И','amounts':[19636661,14676923]},
		])
		nextLine='БЕЗОПАСНОСТИ (825)'
		line=self.lr2.read(rows,line,nextLine)
		self.assertEqual(line,nextLine)
		self.assertEqual(rows,[None,
			{'number':'24.','name':'КОМИТЕТ ПО ПРИРОДОПОЛЬЗОВАНИЮ, ОХРАНЕ ОКРУЖАЮЩЕЙ СРЕДЫ И ОБЕСПЕЧЕНИЮ ЭКОЛОГИЧЕСКОЙ','amounts':[19636661,14676923]},
		])
	def testArkhivnyi(self):
		rows=[None]
		line='2. АРХИВНЫ Й КОМИТЕТ САНКТ-ПЕТЕРБУРГА 335 899.9'
		nextLine='(803)'
		line=self.lr1.read(rows,line,nextLine)
		self.assertEqual(line,nextLine)
		self.assertEqual(rows,[None,
			{'number':'2.','name':'АРХИВНЫЙ КОМИТЕТ САНКТ-ПЕТЕРБУРГА','amounts':[3358999]},
		])
	def testZnaniye(self):
		self.doTestName(self.lr1,[
			'19.39. Субсидия Межрегиональной общественной 0801 4400210 200.0',
			'организации " Общество " Знание"  Санкт-',
			'Петербурга и Ленинградской области"  на ',
			'проведение культурно-образовательных и ',
		],'Субсидия Межрегиональной общественной организации "Общество "Знание" Санкт-Петербурга и Ленинградской области" на')
	def testFund(self):
		self.doTestName(self.lr1,[
			'32.13. Субсидия ОАО "Фонд имущества Санкт- 0114 0921401 10 000,0',
			'Петербурга" на возмещ-е затрат,связан.с осущ-ем ',
			'функций по сопров-ю сделок по приобрет-ю ',
		],'Субсидия ОАО "Фонд имущества Санкт-Петербурга" на возмещ-е затрат,связан.с осущ-ем')
	def testIspolnenieEntry(self):
		lr=record.RecordBuilder(3,2)
		rows=[None]
		line='1. АДМИНИСТРАЦИЯ ГУБЕРНАТОРА САНКТ- 2 112 960.4 2 143 756.6 2 062 085.8 97.59 96.19'
		nextLine='ПЕТЕРБУРГА'
		line=lr.read(rows,line,nextLine)
		self.assertEqual(rows,[None,
			{'number':'1.','name':'АДМИНИСТРАЦИЯ ГУБЕРНАТОРА САНКТ-','amounts':[21129604,21437566,20620858]},
		])
	def testIspolnenieTotal(self):
		lr=record.RecordBuilder(3,2)
		rows=[{}]
		line=' Итого: 431 939 763.4 442 067 920.3 404 032 373.1 93.54 91.40'
		nextLine='                                                                                                                                                                                                                                         '
		line=lr.read(rows,line,nextLine)
		self.assertEqual(rows,[
			{'name':'Итого','amounts':[4319397634,4420679203,4040323731]},
		])
	def testIspolneniePageBreak(self):
		lr=record.RecordBuilder(3,2)
		rows=[None]
		line='7. ЖИЛИЩНЫЙ КОМИТЕТ 15 624 229.3 15 794 610.8 14 855 482.4 95.08 94.05'
		nextLine='Показатели расходов бюджета Санкт-Петербурга за 2011 год'
		line=lr.read(rows,line,nextLine)
		self.assertEqual(rows,[
			None,
			{'number':'7.','name':'ЖИЛИЩНЫЙ КОМИТЕТ','amounts':[156242293,157946108,148554824]},
		])
		nextLine='по ведомственной структуре расходов бюджета Санкт-Петербурга'
		line=lr.read(rows,line,nextLine)
		self.assertEqual(rows,[
			None,
			{'number':'7.','name':'ЖИЛИЩНЫЙ КОМИТЕТ','amounts':[156242293,157946108,148554824]},
			None,
		])
	def testUnmarkedTotal(self):
		lr=record.RecordBuilder(1,quirks={'unmarkedTotal'})
		rows=[{}]
		line='323 653 884.8'
		nextLine='226 Приложение 3'
		line=lr.read(rows,line,nextLine)
		self.assertEqual(rows,[
			{'name':'Итого','amounts':[3236538848]},
		])
	def testUnmarkedTotalWithUndottedNumbersEnabled(self):
		lr=record.RecordBuilder(1,quirks={'unmarkedTotal','undottedNumbers'})
		rows=[{}]
		line='323 653 884.8'
		nextLine='226 Приложение 3'
		line=lr.read(rows,line,nextLine)
		self.assertEqual(rows,[
			{'name':'Итого','amounts':[3236538848]},
		])
	def testUndottedNumber(self):
		lr=record.RecordBuilder(1,quirks={'undottedNumbers'})
		rows=[None]
		line='1 АДМИНИСТРАЦИЯ ГУБЕРНАТОРА САНКТ- 1 501 819.1'
		nextLine='ПЕТЕРБУРГА (801)'
		line=lr.read(rows,line,nextLine)
		self.assertEqual(rows,[None,
			{'number':'1.','name':'АДМИНИСТРАЦИЯ ГУБЕРНАТОРА САНКТ-','amounts':[15018191]},
		])
	def testUndottedNumberPartOnNextLine(self):
		lr=record.RecordBuilder(2,quirks={'undottedNumbers'})
		rows=[None]
		line='18.43. Мероприятия в области здравоохранения, 0904 5220086 455 1 494 500.0 1 499 700.0'
		nextLine='1 спорта и физической культуры, туризма'
		line=lr.read(rows,line,nextLine)
		self.assertEqual(line,'спорта и физической культуры, туризма')
		self.assertEqual(rows,[None,
			{'number':'18.43.1.','name':'Мероприятия в области здравоохранения,','section':'0904','article':'5220086','type':'455','amounts':[14945000,14997000]},
		])
	def testUndottedSplitNumber(self):
		lr=record.RecordBuilder(2,quirks={'undottedNumbers'})
		rows=[None]
		line='17.4.1 Осуществление расходов Российской 0401 5190010 282 173 584.8 172 367.1'
		nextLine='1 Федерации по управлению в области занятости'
		line=lr.read(rows,line,nextLine)
		self.assertEqual(line,'Федерации по управлению в области занятости')
		self.assertEqual(rows,[None,
			{'number':'17.4.11.','name':'Осуществление расходов Российской','section':'0401','article':'5190010','type':'282','amounts':[1735848,1723671]},
		])
	def testUndottedNonsplitNumberFollowedByDigits(self):
		lr=record.RecordBuilder(1,quirks={'undottedNumbers'})
		rows=[None]
		line='45.2 Расходы на реализацию Федерального Закона от 0105 5190009 410.3'
		nextLine='20.08.2004 № 113-ФЗ "О присяжных заседателях'
		line=lr.read(rows,line,nextLine)
		self.assertEqual(rows,[None,
			{'number':'45.2.','name':'Расходы на реализацию Федерального Закона от','section':'0105','article':'5190009','amounts':[4103]},
		])
	def testUndottedNonsplitNumberFollowedByPageBreak(self):
		lr=record.RecordBuilder(1,quirks={'undottedNumbers'})
		rows=[None]
		line='9.9.1 Мероприятия в области жилищного хозяйства 0501 3500001 410 204 843.9'
		nextLine='10 Приложение 3'
		line=lr.read(rows,line,nextLine)
		self.assertEqual(rows,[None,
			{'number':'9.9.1.','name':'Мероприятия в области жилищного хозяйства','section':'0501','article':'3500001','type':'410','amounts':[2048439]},
		])

if __name__=='__main__':
	unittest.main()
