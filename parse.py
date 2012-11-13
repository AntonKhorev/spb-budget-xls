# java -jar pdfbox-app-1.7.1.jar ExtractText -encoding UTF-8 pr-bd-2013-15/pr03-2013-15.pdf

import re

filename='pr03-2013-15.txt'

class Entry:
	def __init__(self,row):
		self.row=row
		self.children={}
		self.number=self.article=self.section=self.type=None
	def parseAmount(self,amountText):
		amount=re.sub('\s|\.','',amountText)
		self.amount=int(amount)
	def addLeaf(self,entry,number):
		n=number.pop(0)
		if len(number)==0:
			if n in self.children:
				raise Exception('duplicate entry')
			self.children[n]=entry
		else:
			if n not in self.children:
				raise Exception('child not found')
			self.children[n].addLeaf(entry,number)
	def formatAmount(self,amount):
		a=str(amount)
		return a[:-1]+'.'+a[-1]
	def print(self):
		checkFailed=False
		if self.children:
			sumAmount=sum(child.amount for child in self.children.values())
			if sumAmount!=self.amount:
				# raise Exception('sum(children)!=amount: '+str(sumAmount)+' != '+str(self.amount))
				checkFailed=True
				n=max(int(n) for n in self.children)+1
				diff=Entry(-1)
				diff.name='???'
				diff.amount=self.amount-sumAmount
				self.children[n]=diff
		print(self.number,'\t',self.name,'\t',self.article,'\t',self.section,'\t',self.type,'\t',self.formatAmount(self.amount),'\t','!='+self.formatAmount(sumAmount) if checkFailed else '')
		for n,entry in sorted(self.children.items()):
			entry.print()

class Spreadsheet:
	def __init__(self):
		self.row=1
		self.root=Entry(self.row)
	def makeEntry(self,number):
		self.row+=1
		entry=Entry(self.row)
		entry.number=number
		number=[int(n) for n in number.split('.') if n!='']
		self.root.addLeaf(entry,number)
		return entry
	def print(self):
		self.root.print()

spreadsheet=Spreadsheet()
entry=None
for line in open(filename,encoding='utf8'):
	m=re.match('((?:\d+\.)+)\s+(?:(\d{7})(\d{4})\s+)?([0-9 ]+\.\d)(.*)',line)
	if m:
		number=m.group(1)
		entry=spreadsheet.makeEntry(number)
		entry.article=m.group(2)
		entry.section=m.group(3)
		entry.parseAmount(m.group(4))
		name_type=m.group(5)
		mm=re.match('(.*)\s(\d\d\d)',name_type)
		if mm:
			entry.name=mm.group(1).strip()
			entry.type=mm.group(2)
		else:
			entry.name=name_type.strip()
			entry.type=None
		continue
	if re.match('\d\d-...-2012',line): # new page
		entry=None
		continue
	m=re.match('([0-9 ]+\.\d)(Итого):',line)
	if m: # total
		spreadsheet.root.name=m.group(2)
		spreadsheet.root.parseAmount(m.group(1))
		continue
	else: # next line of name
		if entry:
			if entry.name[-1]!='-':
				entry.name+=' '
			entry.name+=line.strip()

spreadsheet.print()
