#!/usr/bin/env python3

import glob
import html.parser,urllib.parse
import re

import main

# reads *.htm from hosting and extracts links to files
class Linker:
	def __init__(self,env):
		self.fileLinks=fileLinks={}
		class Parser(html.parser.HTMLParser):
			def handle_starttag(self,tag,attrs):
				nonlocal fileLinks
				if tag!='a':
					return
				for a,v in attrs:
					if a!='href':
						continue
					u=urllib.parse.unquote(v)
					m=re.search(r'(?:csv|xls)/.+\.(?:csv|xls)$',u)
					if m:
						v=v.replace('https://www.dropbox.com/','https://dl.dropbox.com/',1) # dropbox special
						fileLinks[m.group(0)]=v
		for filename in glob.glob(env.rootPath+'/htm/*.htm'):
			with open(filename,encoding='utf-8') as f:
				Parser().feed(f.read())
	def getLink(self,path):
		if path not in self.fileLinks:
			raise Exception(path+' not hosted')
		return self.fileLinks[path]

if __name__=='__main__':
	env=main.Environment(main.loadData())
	linker=Linker(env)
	if not env.hasHtml():
		env.writeHtml(False,linker)
