def toArray(number):
	return [int(n) for n in number.split('.') if n!='']

class START: # symbol
	def split(_=None):
		return []

class NumberSequenceChecker:
	def __init__(self,minDepth,maxDepth=None):
		self.minDepth=minDepth
		self.maxDepth=minDepth if maxDepth is None else maxDepth
	def checkPair(self,prevNumber,number):
		prevArray=toArray(prevNumber)
		array=toArray(number)
		if len(array)>self.maxDepth:
			return False
		if len(array)>len(prevArray)+1:
			return False
		if len(array)>len(prevArray):
			if array!=prevArray+[1]:
				return False
		elif len(prevArray)<self.minDepth:
			return False
		else:
			d=[a-b for a,b in zip(array,prevArray)]
			d[-1]-=1
			if any(d):
				return False
		return True
	def findError(self,sequence):
		"returns number (or START) before invalid (next) number / unexpected sequence end"
		prevNumber=START
		for number in sequence:
			if not self.checkPair(prevNumber,number):
				return prevNumber
			prevNumber=number
		if not self.minDepth<=len(toArray(prevNumber))<=self.maxDepth:
			return prevNumber
		return None
