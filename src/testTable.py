#!/usr/bin/env python3

import unittest

import table

class TestTableBuilder(unittest.TestCase):
	def setUp(self):
		self.data1=[
			{'name':'Total','amounts':[800]},
			{'number':'1.','name':'One','amounts':[300]},
			{'number':'1.1.','name':'One One','section':'1','article':'11','amounts':[100]},
			{'number':'1.1.1.','name':'One One One','section':'1','article':'11','type':'111','amounts':[70]},
			{'number':'1.1.2.','name':'One One Two','section':'1','article':'11','type':'112','amounts':[30]},
			{'number':'1.2.','name':'One Two','section':'1','article':'12','amounts':[200]},
			{'number':'1.2.1.','name':'One Two One','section':'1','article':'12','type':'121','amounts':[200]},
			{'number':'2.','name':'Two','amounts':[500]},
			{'number':'2.1.','name':'Two One','section':'2','article':'21','amounts':[500]},
			{'number':'2.1.1.','name':'Two One One','section':'2','article':'21','type':'211','amounts':[500]},
		]
		self.data1slack=[
			{'name':'Total','amounts':[800]},
			{'number':'1.','name':'One','amounts':[300]},
			{'number':'1.1.','name':'One One','section':'1','article':'11','amounts':[100]},
			{'number':'1.1.1.','name':'One One One','section':'1','article':'11','type':'111','amounts':[69]},
			{'number':'1.1.2.','name':'One One Two','section':'1','article':'11','type':'112','amounts':[30]},
			{'number':'1.2.','name':'One Two','section':'1','article':'12','amounts':[199]},
			{'number':'1.2.1.','name':'One Two One','section':'1','article':'12','type':'121','amounts':[199]},
			{'number':'2.','name':'Two','amounts':[498]},
			{'number':'2.1.','name':'Two One','section':'2','article':'21','amounts':[498]},
			{'number':'2.1.1.','name':'Two One One','section':'2','article':'21','type':'211','amounts':[498]},
		]
		self.total1=[800]
	def test1(self):
		tb=table.TableBuilder(self.data1,self.total1,1)
		rows=list(tb.rows(
			['number','name','section','article','type',('amounts',0,(0,1))],
			useSums=False
		))
		self.assertEqual(rows,[
			[None,		'Total',	None,	None,	None,	'80,0'],
			['1.',		'One',		None,	None,	None,	'30,0'],
			['2.',		'Two',		None,	None,	None,	'50,0'],
		])
	def test2(self):
		tb=table.TableBuilder(self.data1,self.total1,2)
		rows=list(tb.rows(
			['number','name','section','article','type',('amounts',0,(0,1,2))],
			useSums=False
		))
		self.assertEqual(rows,[
			[None,		'Total',	None,	None,	None,	'80,0'],
			['1.',		'One',		None,	None,	None,	'30,0'],
			['1.1.',	'One One',	'1',	'11',	None,	'10,0'],
			['1.2.',	'One Two',	'1',	'12',	None,	'20,0'],
			['2.',		'Two',		None,	None,	None,	'50,0'],
			['2.1.',	'Two One',	'2',	'21',	None,	'50,0'],
		])
	def test3(self):
		tb=table.TableBuilder(self.data1,self.total1,3)
		rows=list(tb.rows(
			['number','name','section','article','type',('amounts',0,(0,1,2,3))],
			useSums=False
		))
		self.assertEqual(rows,[
			[None,		'Total',	None,	None,	None,	'80,0'],
			['1.',		'One',		None,	None,	None,	'30,0'],
			['1.1.',	'One One',	'1',	'11',	None,	'10,0'],
			['1.1.1.',	'One One One',	'1',	'11',	'111',	'7,0'],
			['1.1.2.',	'One One Two',	'1',	'11',	'112',	'3,0'],
			['1.2.',	'One Two',	'1',	'12',	None,	'20,0'],
			['1.2.1.',	'One Two One',	'1',	'12',	'121',	'20,0'],
			['2.',		'Two',		None,	None,	None,	'50,0'],
			['2.1.',	'Two One',	'2',	'21',	None,	'50,0'],
			['2.1.1.',	'Two One One',	'2',	'21',	'211',	'50,0'],
		])
	def test3Sums(self):
		tb=table.TableBuilder(self.data1,self.total1,3)
		rows=list(tb.rows(
			['number','name','section','article','type',('amounts',0,(0,1,2,3))],
			useSums=True
		))
		self.assertEqual(rows,[
			# A		B		C	D	E	F
			[None,		'Total',	None,	None,	None,	'=F2+F8'],	# 1
			['1.',		'One',		None,	None,	None,	'=F3+F6'],	# 2
			['1.1.',	'One One',	'1',	'11',	None,	'=F4+F5'],	# 3
			['1.1.1.',	'One One One',	'1',	'11',	'111',	'7,0'],		# 4
			['1.1.2.',	'One One Two',	'1',	'11',	'112',	'3,0'],		# 5
			['1.2.',	'One Two',	'1',	'12',	None,	'=F7'],		# 6
			['1.2.1.',	'One Two One',	'1',	'12',	'121',	'20,0'],	# 7
			['2.',		'Two',		None,	None,	None,	'=F9'],		# 8
			['2.1.',	'Two One',	'2',	'21',	None,	'=F10'],	# 9
			['2.1.1.',	'Two One One',	'2',	'21',	'211',	'50,0'],	# 10
		])
	def test3Stairs(self):
		tb=table.TableBuilder(self.data1,self.total1,3)
		rows=list(tb.rows(
			['number','name','section','article','type',('amounts',0,(0,)),('amounts',0,(1,)),('amounts',0,(2,)),('amounts',0,(3,))],
			useSums=False
		))
		self.assertEqual(rows,[
			[None,		'Total',	None,	None,	None,	'80,0',	None,	None,	None],
			['1.',		'One',		None,	None,	None,	None,	'30,0',	None,	None],
			['1.1.',	'One One',	'1',	'11',	None,	None,	None,	'10,0',	None],
			['1.1.1.',	'One One One',	'1',	'11',	'111',	None,	None,	None,	'7,0'],
			['1.1.2.',	'One One Two',	'1',	'11',	'112',	None,	None,	None,	'3,0'],
			['1.2.',	'One Two',	'1',	'12',	None,	None,	None,	'20,0',	None],
			['1.2.1.',	'One Two One',	'1',	'12',	'121',	None,	None,	None,	'20,0'],
			['2.',		'Two',		None,	None,	None,	None,	'50,0',	None,	None],
			['2.1.',	'Two One',	'2',	'21',	None,	None,	None,	'50,0',	None],
			['2.1.1.',	'Two One One',	'2',	'21',	'211',	None,	None,	None,	'50,0'],
		])
	def test3StairsSums(self):
		tb=table.TableBuilder(self.data1,self.total1,3)
		rows=list(tb.rows(
			['number','name','section','article','type',('amounts',0,(0,)),('amounts',0,(1,)),('amounts',0,(2,)),('amounts',0,(3,))],
			useSums=True
		))
		self.assertEqual(rows,[
			# A		B		C	D	E	F		G		H		I
			[None,		'Total',	None,	None,	None,	'=SUM(G2:G10)',	None,		None,		None],	# 1
			['1.',		'One',		None,	None,	None,	None,		'=SUM(H3:H7)',	None,		None],	# 2
			['1.1.',	'One One',	'1',	'11',	None,	None,		None,		'=SUM(I4:I5)',	None],	# 3
			['1.1.1.',	'One One One',	'1',	'11',	'111',	None,		None,		None,		'7,0'],	# 4
			['1.1.2.',	'One One Two',	'1',	'11',	'112',	None,		None,		None,		'3,0'],	# 5
			['1.2.',	'One Two',	'1',	'12',	None,	None,		None,		'=SUM(I7:I7)',	None],	# 6
			['1.2.1.',	'One Two One',	'1',	'12',	'121',	None,		None,		None,		'20,0'],# 7
			['2.',		'Two',		None,	None,	None,	None,		'=SUM(H9:H10)',	None,		None],	# 8
			['2.1.',	'Two One',	'2',	'21',	None,	None,		None,		'=SUM(I10:I10)',None],	# 9
			['2.1.1.',	'Two One One',	'2',	'21',	'211',	None,		None,		None,		'50,0'],# 10
		])
	def test3StairsSumsSlack(self):
		tb=table.TableBuilder(self.data1slack,self.total1,3)
		rows=list(tb.rows(
			['number','name','section','article','type',('amounts',0,(0,)),('amounts',0,(1,)),('amounts',0,(2,)),('amounts',0,(3,)),('amounts',0,'slack')],
			useSums=True
		))
		self.assertEqual(rows,[
			# A		B		C	D	E	F			G			H			I	J
			[None,		'Total',	None,	None,	None,	'=SUM(G2:G10)+J1',	None,			None,			None,	'0,2'],	# 1
			['1.',		'One',		None,	None,	None,	None,			'=SUM(H3:H7)+J2',	None,			None,	'0,1'],	# 2
			['1.1.',	'One One',	'1',	'11',	None,	None,			None,			'=SUM(I4:I5)+J3',	None,	'0,1'],	# 3
			['1.1.1.',	'One One One',	'1',	'11',	'111',	None,			None,			None,			'6,9',	None],	# 4
			['1.1.2.',	'One One Two',	'1',	'11',	'112',	None,			None,			None,			'3,0',	None],	# 5
			['1.2.',	'One Two',	'1',	'12',	None,	None,			None,			'=SUM(I7:I7)+J6',	None,	None],	# 6
			['1.2.1.',	'One Two One',	'1',	'12',	'121',	None,			None,			None,			'19,9',	None],	# 7
			['2.',		'Two',		None,	None,	None,	None,			'=SUM(H9:H10)+J8',	None,			None,	None],	# 8
			['2.1.',	'Two One',	'2',	'21',	None,	None,			None,			'=SUM(I10:I10)+J9',	None,	None],	# 9
			['2.1.1.',	'Two One One',	'2',	'21',	'211',	None,			None,			None,			'49,8',	None],	# 10
		])

if __name__=='__main__':
	unittest.main()
