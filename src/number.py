def toArray(number):
	return [int(n) for n in number.split('.') if n!='']

class START: pass # symbol

class NumberSequenceChecker:
	def __init__(self,minDepth,maxDepth=None):
		self.minDepth=minDepth
		self.maxDepth=minDepth if maxDepth is None else maxDepth
	def findError(self,sequence):
		"returns number (or START) before invalid (next) number / unexpected sequence end"
		prevNumber=START
		prevArray=[]
		for number in sequence:
			array=toArray(number)
			if len(array)>self.maxDepth:
				return prevNumber
			if len(array)>len(prevArray)+1:
				return prevNumber
			if len(array)>len(prevArray):
				if array!=prevArray+[1]:
					return prevNumber
			elif len(prevArray)<self.minDepth:
				return prevNumber
			else:
				d=[a-b for a,b in zip(array,prevArray)]
				d[-1]-=1
				if any(d):
					return prevNumber
			prevNumber=number
			prevArray=array
		if not self.minDepth<=len(prevArray)<=self.maxDepth:
			return prevNumber
		return None
