import html

class HtmlWriter:
	class Refs:
		class Ref:
			def __init__(self,number,html):
				self.number=number
				self.html=html
			@property
			def id(self):
				return "ref-"+str(self.number)
			@property
			def ref(self):
				return "<sup><a href='#"+self.id+"'>["+str(self.number)+"]</a></sup>"
			@property
			def body(self):
				return "<div id='"+self.id+"'>"+self.html+"</div>"
		def __init__(self):
			self.refs=[]
		def __iter__(self):
			return self.refs.__iter__()
		def makeRef(self,html):
			ref=self.__class__.Ref(len(self.refs)+1,html)
			self.refs.append(ref)
			return ref

	def __init__(self,linker=None):
		self.linker=linker
		self.isExternal=bool(linker)

	def write(self,filename):
		file=open(filename,'w',encoding='utf-8')
		w=file.write
		e=lambda x: html.escape(str(x))
		a=lambda link,text: "<a href='"+e(link)+"'>"+text+"</a>"
		if self.linker is None:
			af=a
		else:
			af=lambda link,text: a(self.linker.getLink(link),text)
		wtd=lambda x: w("<td>"+x+"</td>")
		wtdrowspan=lambda n,x: w("<td rowspan='"+e(n)+"'>"+x+"</td>")
		def nonFirstWrite():
			first=True
			def wn(s):
				nonlocal first
				if first:
					first=False
					return
				w(s)
			return wn

		w(
"""<!DOCTYPE HTML>
<html>
<head>
<meta charset='utf-8' />
"""
		)
		w("<title>"+self.getTitle()+"</title>\n")
		w(
"""<style>
nav {
	background: #246;
}
nav ul {
	margin: 0;
	padding: 0;
}
nav li {
	display: inline-block;
	list-style: none;
	margin: 1em 0 1em 2em;
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
			('db.html','БД'),
		):
			w("<li>"+a(link,text)+"</li>")
		w("</ul></nav>\n")

		ctx=locals()
		def makeFns(fnStr):
			"function to make w(), a(), e() and likes"
			return tuple(ctx[fn] for fn in fnStr.split(','))

		self.writeContents(makeFns)

		w(
"""</body>
</html>
"""
		)

		file.close()
