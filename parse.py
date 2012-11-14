# java -jar pdfbox-app-1.7.1.jar ExtractText -encoding UTF-8 pr-bd-2013-15/pr03-2013-15.pdf

import re
import csv

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
		return a[:-1]+','+a[-1]
	def scanRows(self):
		if not self.children:
			self.rowSpan=(self.row,self.row+1)
			return
		rows=[]
		for child in self.children.values():
			child.scanRows()
			if child.rowSpan is None:
				self.rowSpan=None
				return
			rows.append(child.rowSpan)
		rows.sort()
		if self.row+1!=rows[0][0]:
			self.rowSpan=None
			return
		for i in range(1,len(rows)):
			if rows[i-1][1]!=rows[i][0]:
				self.rowSpan=None
				return
		self.rowSpan=(rows[0][0]-1,rows[-1][1])

	def write(self,writer,useSums,depth=0):
		if useSums and self.children:
			sumAmount=sum(child.amount for child in self.children.values())
			if sumAmount!=self.amount:
				raise Exception('sum(children)!=amount: '+str(sumAmount)+' != '+str(self.amount))
				# checkFailed=True
				# n=max(int(n) for n in self.children)+1
				# diff=Entry(-1)
				# diff.name='???'
				# diff.amount=self.amount-sumAmount
				# self.children[n]=diff
			columnLetter=chr(ord('F')+depth+1)
			if self.rowSpan is None:
				am='='+'+'.join(columnLetter+str(entry.row) for n,entry in sorted(self.children.items()))
			else:
				am='=SUM('+columnLetter+str(self.rowSpan[0]+1)+':'+columnLetter+str(self.rowSpan[1]-1)+')'
		else:
			am=self.formatAmount(self.amount)
		if useSums:
			amList=[None]*depth+[am]
		else:
			amList=[am]
		writer.writerow([self.number,self.name,self.article,self.section,self.type]+amList)
		for n,entry in sorted(self.children.items()):
			entry.write(writer,useSums,depth+1)

class Spreadsheet:
	def __init__(self,depthLimit=10,useSums=True):
		self.row=2 # row 1 for header
		self.depthLimit=depthLimit
		self.useSums=useSums
		self.root=Entry(self.row)
	def makeEntry(self,numberStr):
		number=[int(n) for n in numberStr.split('.') if n!='']
		if len(number)>self.depthLimit:
			return Entry(-1) # throwaway entry
		self.row+=1
		entry=Entry(self.row)
		entry.number=numberStr
		self.root.addLeaf(entry,number)
		return entry
	def read(self,filename):
		entry=None
		for line in open(filename,encoding='utf8'):
			m=re.match('((?:\d+\.)+)\s+(?:(\d{6}[0-9а-я])(\d{4})\s+)?([0-9 ]+\.\d)(.*)',line)
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
			m=re.match('^\d\d\d$',line) # type on separate line
			if m:
				if entry:
					entry.type=m.group(0)
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
		self.root.scanRows()
	def write(self,filename):
		writer=csv.writer(open(filename,'w',newline='',encoding='utf8'),quoting=csv.QUOTE_NONNUMERIC)
		writer.writerow(['Номер','Наименование','Код раздела','Код целевой статьи','Код вида расходов','Сумма (тыс. руб.)'])
		self.root.write(writer,self.useSums)

for depth,sums,inputFilename,outputFilename in [
	(1,False,'pr03-2013-15.txt','pr03-2013-15(1).csv'),
	(2,False,'pr03-2013-15.txt','pr03-2013-15(2).csv'),
	(3,False,'pr03-2013-15.txt','pr03-2013-15(3).csv'),
	(1,True ,'pr03-2013-15.txt','pr03-2013-15(1,sums).csv'),
	(2,True ,'pr03-2013-15.txt','pr03-2013-15(2,sums).csv'),
	(3,True ,'pr03-2013-15.txt','pr03-2013-15(3,sums).csv'),
]:
	spreadsheet=Spreadsheet(depth,sums)
	spreadsheet.read(inputFilename)
	spreadsheet.write(outputFilename)
