# java -jar pdfbox-app-1.7.1.jar ExtractText -encoding UTF-8 pr-bd-2013-15/pr03-2013-15.pdf

import re

filename='pr03-2013-15.txt'

class Entry:
	def print(self):
		print(self.number,'\t',self.name,'\t',self.article,'\t',self.section,'\t',self.type,'\t',self.amount)

entry=None
for line in open(filename,encoding='utf8'):
	m=re.match('((?:\d+\.)+)\s+(?:(\d{7})(\d{4})\s+)?([0-9 ]+\.\d)(.*)',line)
	if m:
		if entry:
			entry.print()
		entry=Entry()
		entry.number=m.group(1)
		entry.article=m.group(2)
		entry.section=m.group(3)
		entry.amount=m.group(4)
		name_type=m.group(5)
		mm=re.match('(.*)\s(\d\d\d)',name_type)
		if mm:
			entry.name=mm.group(1).strip()
			entry.type=mm.group(2)
		else:
			entry.name=name_type.strip()
			entry.type=None
		continue
	if re.match('\d\d-...-2012',line):
		if entry:
			entry.print()
		entry=None
	else:
		if entry:
			if entry.name[-1]!='-':
				entry.name+=' '
			entry.name+=line.strip()
if entry:
	entry.print()
