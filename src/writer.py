import collections
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

	def __init__(self,env):
		self.env=env

	def write(self,filename):
		file=open(filename,'w',encoding='utf-8')
		w=file.write
		e=lambda x: html.escape(str(x))
		a=lambda link,text: "<a href='"+e(link)+"'>"+text+"</a>"
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
		refs=HtmlWriter.Refs()

		w(
"""<!DOCTYPE HTML>
<html>
<head>
<meta charset='utf-8'>
<title>Ведомственные структуры расходов бюджета Санкт-Петербурга в csv и xls</title>
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
<h1>Ведомственные структуры расходов бюджета Санкт-Петербурга</h1>
"""
		)
		yearLaws=collections.defaultdict(list)
		for law in self.env.laws:
			yearLaws[law.year].append(law)
		w("<p>Документы для годов: ")
		wn=nonFirstWrite()
		for year in sorted(yearLaws):
			wn(", ")
			w(a("#"+year,e(year)))
		w(".</p>\n")

		refCsv=refs.makeRef("В кодировке utf-8. Числа с десятичной запятой, потому что в таком формате их читают русские версии электронных таблиц.")
		w("<table>\n")
		w("<thead>\n")
		w("<tr><th>год</th><th>закон</th><th>исходные документы</th><th>приложение</th><th>csv"+refCsv.ref+" без формул</th><th>csv"+refCsv.ref+" с формулами</th><th>xls</th></tr>\n")
		w("</thead>\n")
		for year,laws in sorted(yearLaws.items()):
			w("<tbody id='"+e(year)+"'>\n");
			w("<tr>")
			wtdrowspan(len(laws)*2,e(year))
			wn=nonFirstWrite()
			for law in laws:
				wn("<tr>")
				wtdrowspan(2,"<span title='"+e(law.title)+"'>"+e(law.description)+"</span>")
				wtdrowspan(2,a(law.viewUrl,"страница")+" "+a(law.downloadUrl,"архив")+" "+a(law.zipPath,"копия"))
				wn2=nonFirstWrite()
				for doc in law.documents: # assumes 2 documents
					wn2("<tr>")
					w("<td><span title='"+"Приложение "+e(doc.appendixNumber)+". "+e(doc.title)+"'>")
					if len(doc.forYears)==1:
						w("расходы "+e('-'.join(doc.forYears)))
					else:
						w("план "+e('-'.join(doc.forYears)))
					w("</span></td>")
					def matrix(path):
						w("<td><pre><code>"+
							a(path(1,False),"1.")+"<br />"+
							a(path(2,False),"1.2.")+"   "+a(path(2,True),"1.2.")+"<br />"+
							a(path(3,False),"1.2.3.")+"      "+a(path(3,True),"1.2.3.")+
						"</code></pre></td>")
					matrix(lambda l,s: doc.getCsvPath(l,s,False))
					matrix(lambda l,s: doc.getCsvPath(l,s,True))
					matrix(doc.getXlsPath)
					w("</tr>\n")
			w("</tbody>\n");
		w("</table>\n")

		w(
"""<h2>Примечания</h2>
<ol>
"""
		)
		for ref in refs:
			w("<li>"+ref.body+"</li>")
		w(
"""</ol>
</body>
</html>
"""
		)

		file.close()
