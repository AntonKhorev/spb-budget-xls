import glob
import html.parser,urllib.parse
import re

import data,main

# reads *.htm from hosting and extracts links to files
class Linker:
	def parse(self,filename):
		self.fileLinks=fileLinks={}
		class Parser(html.parser.HTMLParser):
			def handle_starttag(self,tag,attrs):
				if tag!='a':
					return
				for a,v in attrs:
					if a!='href':
						continue
					u=urllib.parse.unquote(v)
					m=re.search(r'(?:csv|xls)/.+\.(?:csv|xls)$',u)
					if m:
						fileLinks[m.group(0)]=v
		with open(filename,encoding='utf-8') as f:
			Parser().feed(f.read())
		print(fileLinks)
	def __init__(self,env):
		for filename in glob.glob(env.rootPath+'/htm/*.htm'):
			self.parse(filename)

if __name__=='__main__':
	env=main.Environment(data.data)
	linker=Linker(env)
	# if not env.hasHtml():
		# env.writeHtml(linker)
