import html

class HtmlPage:
	def __init__(self,content):
		self.content=content

	def write(self,filename):
		file=open(filename,'w',encoding='utf-8')
		w=file.write
		e=lambda t: html.escape(str(t))
		def a(link,text,title=None,cls=None):
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
<style>
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
