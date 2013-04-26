import collections
import html

class HtmlWriter:
	def __init__(self,env):
		self.env=env
	def write(self,filename):
		file=open(filename,'w',encoding='utf-8')
		w=file.write
		e=lambda x: html.escape(str(x))
		a=lambda link,text: "<a href='"+e(link)+"'>"+e(text)+"</a>"
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
<meta charset='utf-8'>
<title>Ведомственные структуры расходов бюджета Санкт-Петербурга в csv и xls</title>
<style>
th,td {
	vertical-align: top;
}
</style>
</head>
<body>
<h1>Ведомственные структуры расходов бюджета Санкт-Петербурга</h1>
<table>
<tr><th>год</th><th>закон</th><th>исходные документы</th><th>приложение</th><th>csv без формул</th><th>csv с формулами</th><th>xls</th></tr>
"""
		)
		yearLaws=collections.defaultdict(list)
		for law in self.env.laws:
			yearLaws[law.year].append(law)
		for year,laws in sorted(yearLaws.items()):
			w("<tr>")
			wtdrowspan(len(laws)*2,e(year))
			wn=nonFirstWrite()
			for law in laws:
				wn("<tr>")
				wtdrowspan(2,e(law.description))
				wtdrowspan(2,a(law.viewUrl,"страница")+" "+a(law.downloadUrl,"архив")+" "+a(law.zipPath,"копия"))
				wn2=nonFirstWrite()
				for doc in law.documents: # assumes 2 documents
					wn2("<tr>")
					if len(doc.forYears)==1:
						wtd("расходы "+e('-'.join(doc.forYears)))
					else:
						wtd("план "+e('-'.join(doc.forYears)))
					def matrix(path):
						w("<td><pre><code>"+
							a(path(1,False),"1.")+"<br />"+
							a(path(2,False),"1.2.")+"    "+a(path(2,True),"1.2.")+"<br />"+
							a(path(3,False),"1.2.3.")+"          "+a(path(3,True),"1.2.3.")+
						"</code></pre></td>")
					matrix(lambda l,s: doc.getCsvPath(l,s,False))
					matrix(lambda l,s: doc.getCsvPath(l,s,True))
					matrix(doc.getXlsPath)
					w("</tr>\n")
		w(
"""</table>
</body>
</html>
"""
		)
		file.close()
