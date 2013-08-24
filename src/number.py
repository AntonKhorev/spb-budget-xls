def toArray(number):
	return [int(n) for n in number.split('.') if n!='']

class START: pass # symbol

class NumberSequenceChecker:
	def __init__(self,depth):
		self.depth=depth
	def findError(self,sequence):
		"returns number (or START) before invalid (next) number / unexpected sequence end"
		prevNumber=START
		prevArray=[]
		for number in sequence:
			array=toArray(number)
			if len(prevArray)<self.depth:
				if array!=prevArray+[1]:
					return prevNumber
			else:
				if len(array)>self.depth:
					return prevNumber
				d=[a-b for a,b in zip(array,prevArray)]
				d[-1]-=1
				if any(d):
					return prevNumber
			prevNumber=number
			prevArray=array
		if len(prevArray)!=self.depth:
			return prevNumber
		return None
