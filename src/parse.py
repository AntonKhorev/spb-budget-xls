import os.path, glob
import re, csv
import itertools

class Entry:
	def __init__(self,row):
		self.row=row
		self.children={}
		self.number=self.name=self.article=self.section=self.type=None
		self.amounts={}
	def appendName(self,name):
		if self.name is None:
			self.name=name.strip()
		else:
			if self.name[-1]!='-' or self.name[-2]==' ':
				self.name+=' '
			self.name+=name.strip()
	def parseAmount(self,amountText,key=0):
		amount=re.sub('\s|\.','',amountText)
		self.amounts[key]=int(amount)
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

	def write(self,writer,useSums,depthLimit,depth=0):
		if useSums and self.children:
			sumAmounts={}
			for child in self.children.values():
				for k,v in child.amounts.items():
					if k not in sumAmounts:
						sumAmounts[k]=0
					sumAmounts[k]+=v
			if sumAmounts!=self.amounts:
				raise Exception('sum(children)!=amount: '+str(sumAmounts)+' != '+str(self.amounts))
			# amounts to write
			ams=[]
			for i,(k,v) in enumerate(sorted(self.amounts.items())):
				columnLetter=chr(ord('F')+depth+1+i*(depthLimit+1))
				if self.rowSpan is None:
					ams.append('='+'+'.join(columnLetter+str(entry.row) for n,entry in sorted(self.children.items())))
				else:
					ams.append('=SUM('+columnLetter+str(self.rowSpan[0]+1)+':'+columnLetter+str(self.rowSpan[1]-1)+')')
		else:
			ams=[self.formatAmount(v) for k,v in sorted(self.amounts.items())]
		if useSums:
			amList=list(itertools.chain.from_iterable([None]*depth+[am]+[None]*(depthLimit-depth) for am in ams))
		else:
			amList=ams
		writer.writerow([self.number,self.name,self.article,self.section,self.type]+amList)
		for n,entry in sorted(self.children.items()):
			entry.write(writer,useSums,depthLimit,depth+1)
	def __str__(self):
		return 'number:'+str(self.number)+'; name:'+str(self.name)+'; amounts:'+str(self.amounts)

class Spreadsheet:
	def __init__(self,depthLimit=3,useSums=True):
		self.row=2 # row 1 for header
		self.depthLimit=depthLimit
		self.useSums=useSums
		self.root=Entry(self.row)
		self.amountHeader=['Сумма (тыс. руб.)']
	def makeEntry(self,numberStr):
		number=[int(n) for n in numberStr.split('.') if n!='']
		if len(number)>self.depthLimit:
			return Entry(-1) # throwaway entry
		self.row+=1
		entry=Entry(self.row)
		entry.number=numberStr
		self.root.addLeaf(entry,number)
		return entry
	def read1(self,filename): # for pr03-2013-15.txt, no sorting
		entry=None
		for line in open(filename,encoding='utf8'):
			m=re.match('((?:\d+\.)+)\s+(?:(\d{6}[0-9а-я])(\d{4})\s+)?([0-9 ]+\.\d)(.*)',line)
			if m:
				number=m.group(1)
				entry=self.makeEntry(number)
				entry.article=m.group(2)
				entry.section=m.group(3)
				entry.parseAmount(m.group(4))
				name_type=m.group(5)
				mm=re.match('(.*)\s(\d\d\d)',name_type)
				if mm:
					entry.appendName(mm.group(1))
					entry.type=mm.group(2)
				else:
					entry.appendName(name_type)
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
				self.root.name=m.group(2)
				self.root.parseAmount(m.group(1))
				continue
			else: # next line of name
				if entry:
					entry.appendName(line)
		self.root.scanRows()
	def read2(self,filename,nCols=1): # for pr04-2013-15.txt, no sorting - FIXME why no sorting? read1 was for no sorting; read2 was for sorting?
		entry=None
		amPattern='\s([0-9 ]+\.\d)'*nCols+'$'
		arPattern='\s(\d{4})\s(\d{6}[0-9а-я])'
		for line in open(filename,encoding='utf8'):
			m=re.match('^((?:\d+\.)+)\s+(.*)$',line)
			if m:
				number=m.group(1)
				rest=m.group(2)
				nc=number.count('.')
				if nc==1:
					m=re.match('^(.*?)'+amPattern,rest)
					if m:
						entry=self.makeEntry(number)
						entry.appendName(m.group(1))
						for i in range(nCols):
							entry.parseAmount(m.group(i+2),i)
						continue
				elif nc==2:
					m=re.match('^(.*?)'+arPattern+amPattern,rest)
					if m:
						entry=self.makeEntry(number)
						entry.appendName(m.group(1))
						entry.section=m.group(2)
						entry.article=m.group(3)
						for i in range(nCols):
							entry.parseAmount(m.group(i+4),i)
						continue
				elif nc==3:
					m=re.match('^(.*?)'+arPattern+'\s(\d{3})'+amPattern,rest)
					if m:
						entry=self.makeEntry(number)
						entry.appendName(m.group(1))
						entry.section=m.group(2)
						entry.article=m.group(3)
						entry.type=m.group(4)
						for i in range(nCols):
							entry.parseAmount(m.group(i+5),i)
						continue
				else:
					raise Exception('unsupported number')
			m=re.match('^(Итого):'+amPattern,line)
			if m: # total
				self.root.name=m.group(1)
				for i in range(nCols):
					self.root.parseAmount(m.group(i+2),i)
				continue
			if re.match('^\d+\s+Приложение',line): # new page
				entry=None
				continue
			if entry: # next line of name
				entry.appendName(line)
		self.root.scanRows()
	def setAmountHeader(self,header):
		self.amountHeader=list(itertools.chain.from_iterable([v]+[None]*self.depthLimit for k,v in sorted(header.items())))
	def write(self,filename):
		writer=csv.writer(open(filename,'w',newline='',encoding='utf8'),quoting=csv.QUOTE_NONNUMERIC)
		writer.writerow(['Номер','Наименование','Код раздела','Код целевой статьи','Код вида расходов']+self.amountHeader)
		self.root.write(writer,self.useSums,self.depthLimit)

def writeVersions(outputDirectory,inputFilename,nCols):
	for sums in (False,True):
		for depth in range(1,4):
			outputFilename=outputDirectory+'/'+os.path.basename(inputFilename[:-4])+'('+str(depth)+(',sums' if sums else '')+').csv'
			spreadsheet=Spreadsheet(depth,sums)
			spreadsheet.read2(inputFilename,nCols)
			# TODO add column headers
			# example for pr04-2013-15.txt:
			# spreadsheet.setAmountHeader({0:'Плановый период 2014 г. (тыс. руб.)',1:'Плановый период 2015 г. (тыс. руб.)'})
			# TODO add document name somewhere
			spreadsheet.write(outputFilename)

root=os.path.realpath(
	os.path.dirname(os.path.realpath(__file__))+'/..'
)
for filename in glob.glob(root+'/txt/*.txt'):
	nCols=1 # TODO detect # of cols
	writeVersions(root+'/csv',filename,nCols)
