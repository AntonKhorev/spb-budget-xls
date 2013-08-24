#!/usr/bin/env python3

import unittest

import number

class TestNumberSequenceChecker(unittest.TestCase):
	def setUp(self):
		self.nsc3=number.NumberSequenceChecker(3)
	def testOk(self):
		e=self.nsc3.findError(['1.','1.1.','1.1.1.','1.2.','1.2.1.','2.','2.1.','2.1.1.'])
		self.assertIsNone(e)
	def testOk2(self):
		e=self.nsc3.findError(['1.','1.1.','1.1.1.','2.','2.1.','2.1.1.'])
		self.assertIsNone(e)
	def testNotDeepEnough(self):
		e=self.nsc3.findError(['1.','1.1.','1.2.','1.2.1.','2.','2.1.','2.1.1.'])
		self.assertEqual(e,'1.1.')
	def testSkippedNumber(self):
		e=self.nsc3.findError(['1.','1.1.','1.1.1.','1.3.','1.3.1.','3.','3.1.','3.1.1.'])
		self.assertEqual(e,'1.1.1.')
	def testUnexpectedEnd(self):
		e=self.nsc3.findError(['1.','1.1.','1.1.1.','1.2.','1.2.1.','2.','2.1.'])
		self.assertEqual(e,'2.1.')
	def testWrongStart(self):
		e=self.nsc3.findError(['2.','2.1.','2.1.1.'])
		self.assertEqual(e,number.START)

if __name__=='__main__':
	unittest.main()
