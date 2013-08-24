import sys

import number

class TableBuilder:
	def __init__(self,data,totalAmounts,depthLimit):
		# need to know depth limit here to assign row numbers

		# make entries
		iRow=0
		for i,row in enumerate(data):
			if row is None:
				continue
			entry=Entry(iRow,row)
			if i==0:
				self.root=entry
			else:
				numberArray=number.toArray(row['number'])
				if len(numberArray)>depthLimit:
					continue
				try:
					self.root.addLeaf(entry,numberArray)
				except Exception as e:
					tb=sys.exc_info()[2]
					raise Exception(str(e)+' in entry number '+row['number']).with_traceback(tb)
			iRow+=1

		self.root.makeRowSpans()
		self.root.calculateSlacks()
		for i,totalAmount in enumerate(totalAmounts):
			self.root.checkAmount(totalAmount,i)

		self.nKeys=len(totalAmounts)

	def rows(self,columns,useSums,rowOffset=1):
		# stairs specified by columns

		def cl(i):
			return chr(ord('A')+i)

		columnLetters=[{} for i in range(self.nKeys)]
		hasStairs=[True for i in range(self.nKeys)]
		for i,column in enumerate(columns):
			if type(column) is not tuple: continue
			name,key,depths=column
			if name!='amounts': continue
			if depths=='slack':
				columnLetters[key]['slack']=cl(i)
			else:
				# TODO consider allowing depth 0 sharing the same column with another depth in 'stairs' mode
				if len(depths)>1:
					hasStairs[key]=False
				for depth in depths:
					columnLetters[key][depth]=cl(i)

		def rec(entry,depth=0):
			def formatAmount(amount):
				a=str(amount)
				if len(a)==1:
					return '0,'+a
				else:
					return a[:-1]+','+a[-1]

			def row(r):
				return str(r+rowOffset)

			def amount(key):
				if useSums and entry.children:
					c=columnLetters[key][depth+1]
					if hasStairs[key] and entry.rowSpan is not None:
						formula='=SUM('+c+row(entry.rowSpan[0]+1)+':'+c+row(entry.rowSpan[1]-1)+')'
					else:
						formula='='+'+'.join(
							c+row(child.iRow) for n,child in sorted(entry.children.items()) if child.isVisible()
						)
					if 'slack' in columnLetters[key]:
						formula+='+'+columnLetters[key]['slack']+row(entry.iRow)
					return formula
				else:
					return formatAmount(entry.amounts[key])

			def cell(column):
				if column=='number':
					return entry.number
				elif column=='name':
					return entry.name
				elif column=='section':
					return entry.section
				elif column=='article':
					return entry.article
				elif column=='type':
					return entry.type
				elif column=='OSGU':
					return entry.OSGU
				elif type(column) is tuple:
					name,key,depths=column
					if name!='amounts':
						raise Exception('unknown complex column '+str(name))
					elif depths=='slack':
						if entry.slacks[key]:
							return formatAmount(entry.slacks[key])
					elif depth in depths:
						return amount(key)
				else:
					raise Exception('unknown column '+str(column))
				return None

			if entry.isVisible():
				for key,slack in enumerate(entry.slacks):
					if slack and 'slack' not in columnLetters[key]:
						raise Exception('slack present and no clack column given for record '+str(entry.number))
				yield [cell(column) for column in columns]

			for n,child in sorted(entry.children.items()):
				for row in rec(child,depth+1):
					yield row

		for row in rec(self.root):
			yield row

# TODO don't need this class
class Entry:
	def __init__(self,iRow,row):
		self.iRow=iRow # -1 for invisible
		self.children={}
		self.number=row.get('number')
		self.name=row.get('name')
		self.article=row.get('article')
		self.section=row.get('section')
		self.type=row.get('type')
		self.OSGU=row.get('OSGU')
		self.amounts=row['amounts']

	def isVisible(self):
		return self.iRow>=0

	def checkAmount(self,amount,key=0):
		if amount!=self.amounts[key]:
			raise Exception("amount doesn't match")

	def addLeaf(self,entry,numberArray):
		n=numberArray.pop(0)
		if len(numberArray)==0:
			if n in self.children:
				raise Exception('duplicate entry '+str(entry.number))
			self.children[n]=entry
		else:
			if n not in self.children: # missing entry of zero sum:
				self.children[n]=Entry(-1,{'amounts':[0]*len(entry.amounts)})
			self.children[n].addLeaf(entry,numberArray)

	def makeRowSpans(self):
		rows=[]
		for child in self.children.values():
			child.makeRowSpans()
			if child.rowSpan is None:
				self.rowSpan=None
				return
			rows.append(child.rowSpan)
		if not rows:
			if self.isVisible():
				self.rowSpan=(self.iRow,self.iRow+1)
				return
			else:
				self.rowSpan=None
				return
		rows.sort()
		if self.isVisible() and self.iRow+1!=rows[0][0]:
			self.rowSpan=None
			return
		for i in range(1,len(rows)):
			if rows[i-1][1]!=rows[i][0]:
				self.rowSpan=None
				return
		if self.isVisible():
			self.rowSpan=(rows[0][0]-1,rows[-1][1])
		else:
			self.rowSpan=(rows[0][0],rows[-1][1])

	def calculateSlacks(self):
		self.slacks=[0]*len(self.amounts)
		if not self.children:
			return
		sumAmounts=[0]*len(self.amounts)
		for child in self.children.values():
			for k,v in enumerate(child.amounts):
				sumAmounts[k]+=v
		self.slacks=[se-su for se,su in zip(self.amounts,sumAmounts)]
		for n,entry in sorted(self.children.items()):
			entry.calculateSlacks()

	def __str__(self):
		return 'number:'+str(self.number)+'; name:'+str(self.name)+'; amounts:'+str(self.amounts)
