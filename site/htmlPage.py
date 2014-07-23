#
# function names:
# w = write
# e = escape
# a = link
# af = link to external file (requires linker)
#
# arg names:
# t = raw text
# x = html text
#

import html

class HtmlPage:
	def __init__(self,link,title,content,linker=None):
		self.link=link
		self.title=title
		self.content=content
		self.linker=linker
		self.isExternal=bool(linker)

	def write(self,filename):
		file=open(filename,'w',encoding='utf-8')
		def w(x):
			file.write(self.linker.findAndProcessLinks(x))
		e=lambda t: html.escape(str(t))
		def a(link,text,title=None,cls=None):
			# { temporary difference
			if self.isExternal and link=='index.html':
				link='.'
			# } temporary difference
			r="<a href='"+e(link)+"'"
			if cls is not None:
				r+=" class='"+e(cls)+"'"
			if title is not None:
				r+=" title='"+e(title)+"'"
			r+=">"+text+"</a>"
			return r
		def af(link,text,title=None):
			return a(link,text,title,'file')
		def ae(link,text,title=None):
			return a(link,text,title,'external')
		def wtd(x=''):
			w("<td>"+x+"</td>")
		wtdrowspan=lambda n,x: w("<td rowspan='"+e(n)+"'>"+x+"</td>")
		def nonFirstWrite():
			first=True
			def wn(x):
				nonlocal first
				if first:
					first=False
					return
				w(x)
			return wn

		w(
"""<!DOCTYPE HTML>
<html>
<head>
<meta charset='utf-8' />
"""
		)
		w("<title>"+self.title+"</title>\n")
		w(
"""<style>
nav {
	background: #246;
	color: #DDD;
}
nav ul {
	margin: 0;
	padding: 1em;
}
nav li {
	display: inline-block;
	list-style: none;
	padding: 0 1em;
}
nav li.active {
	background: #48C;
	color: #FFF;
}
nav :link, nav :visited {
	color: #DDD;
}
nav :link:hover, nav :visited:hover {
	color: #FFF;
}
:target {
	background: #FFC;
}
sup {
	font-size: .7em;
}
sup :link {
	text-decoration: none;
}
sup :link:hover {
	text-decoration: underline;
}
table {
	border: none;
	border-collapse: collapse;
}
td {
	vertical-align: top;
}
th {
	vertical-align: bottom;
}
th,td {
	padding: .5em;
	border-left: dotted 1px gray;
}
tbody tr:first-child td {
	border-top: dotted 1px gray;
}
thead tr:first-child th:first-child,
tbody tr:first-child td:first-child {
	border-left: none;
}
span {
	border-bottom: 1px gray dotted;
}
</style>
</head>
<body>
"""
		)
		w("<nav><ul>")
		for link,text in (
			('index.html','Главная'),
			('xls.html','Таблицы расходов из pdf'),
			('db.html','БД расходов из разных источников'),
			('fincom.html','Что есть на сайте Комитета'),
		):
			if link==self.link:
				w("<li class='active'>"+text+"</li>")
			else:
				w("<li>"+a(link,text)+"</li>")
		w("</ul></nav>\n")

		ctx=locals()
		def makeFns(fnStr):
			"function to make w(), a(), e() and likes"
			return tuple(ctx[fn] for fn in fnStr.split(','))

		self.content(makeFns)

		w(
"""</body>
</html>
"""
		)

		file.close()

def importContent(filename):
	def content(makeFns):
		w,=makeFns('w')
		with open(filename,encoding='utf-8') as file:
			inside=0
			for line in file:
				if line=='<body>\n':
					inside+=1
				elif line=='</body>\n':
					inside-=1
				if inside>0:
					# TODO translate links
					w(line)
	return content
