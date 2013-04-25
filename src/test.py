import unittest

import reader

class TestLineReader(unittest.TestCase):
	def setUp(self):
		self.text1=[
			"1. АДМИНИСТРАЦИЯ ГУБЕРНАТОРА САНКТ- 2 114 774,1",
			"ПЕТЕРБУРГА (801)",
			"1.1. Расходы на содержание главы Правительства 0102 0010008 2 026,0",
			"Санкт-Петербурга",
			"1.1.1. Выполнение функций государственными органами 0102 0010008 012 2 026,0",
			"1.2. Содержание исполнительного органа 0114 0010009 984 695,5",
		]
		self.lr1=reader.LineReader(1)
		self.lr2=reader.LineReader(2)
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

if __name__=='__main__':
	unittest.main()
