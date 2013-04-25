import collections
import html

class HtmlWriter:
	def __init__(self,env):
		self.env=env
	def write(self,filename):
		file=open(filename,'w',encoding='utf-8')
		w=file.write
		e=lambda x: html.escape(str(x))
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
<table>
<tr><th>год</th><th>закон</th></tr>
"""
		)
		yearLaws=collections.defaultdict(list)
		for law in self.env.laws:
			yearLaws[law.year].append(law)
		for year,laws in sorted(yearLaws.items()):
			w("<tr>")
			w("<td rowspan='"+e(len(laws))+"'>"+e(year)+"</td>")
			wn=nonFirstWrite()
			for law in laws:
				wn("<tr>")
				w("<td>"+e(law.description)+"</td>")
				w("</tr>\n")
		w(
"""</table>
</body>
</html>
"""
		)
		file.close()
