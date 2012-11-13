# java -jar pdfbox-app-1.7.1.jar ExtractText -encoding UTF-8 pr-bd-2013-15/pr03-2013-15.pdf

import re

filename='pr03-2013-15.txt'
for line in open(filename,encoding='utf8'):
	m=re.match('((?:\d+\.)+)\s+(?:(\d{7})(\d{4})\s+)?([0-9 ]+\.\d)(.*)',line)
	if m:
		number=m.group(1)
		article=m.group(2)
		section=m.group(3)
		amount=m.group(4)
		name_type=m.group(5)
		mm=re.match('(.*)\s(\d\d\d)',name_type)
		if mm:
			name=mm.group(1)
			type=mm.group(2)
		else:
			name=name_type
			type=None
		print(number,'\t',name,'\t',article,'\t',section,'\t',type,'\t',amount)
