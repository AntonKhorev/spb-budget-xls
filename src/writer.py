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

	def write(self,filename,zipCopy,linker=None):
		file=open(filename,'w',encoding='utf-8')
		w=file.write
		e=lambda x: html.escape(str(x))
		a=lambda link,text: "<a href='"+e(link)+"'>"+text+"</a>"
		if linker is None:
			af=a
		else:
			af=lambda link,text: a(linker.getLink(link),text)
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
<title>Ведомственная структура расходов бюджета Санкт-Петербурга в csv и xls</title>
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
<h1>Ведомственная структура расходов бюджета Санкт-Петербурга</h1>
"""
		)

		w("<p>Данные извлечены автоматически"+refs.makeRef(
			a("https://github.com/AntonKhorev/BudgetSpb","Исходный код программы для извлечения")+"."
		).ref+" из тесктов законов, опубликованных на сайте "+a("http://www.fincom.spb.ru/","Комитета финансов Санкт-Петербурга")+".</p>\n")

		w("<p>Последнее обновление: 04.06.2013."+refs.makeRef(
			"<dl>"
			"<dt>31.05.2013</dt><dd>Добавлен закон 1-й корректировки бюджета 2013 г. и закон об исполнении бюджета 2011 г.</dd>"
			"<dt>04.06.2013</dt><dd>Добавлены законы 2009—2010 гг.</dd>"
			"</dl>"
		).ref+"</p>\n")

		yearLaws=collections.defaultdict(list)
		for law in self.env.laws:
			yearLaws[law.year].append(law)
		w("<p>Документы для годов: ")
		wn=nonFirstWrite()
		for year in sorted(yearLaws):
			wn(", ")
			w(a("#"+year,e(year)))
		w(".</p>\n")

		refData=refs.makeRef(
			"<pre><code>"
			"1.                  \<br />"
			"1.2.   1.2.          ) разные уровни раскрытия<br />"
			"1.2.3.      1.2.3.  /<br />"
			"  |             \<br />"
			"«столбиком»   «лесенкой» — в этом варианте проще формулы для суммирования"
			"</code></pre>"
		)
		refCsv=refs.makeRef("В кодировке utf-8. Числа с десятичной запятой, потому что в таком формате их читают русские версии электронных таблиц.")
		w("<table>\n")
		w("<thead>\n")
		w("<tr><th rowspan='2'>год</th><th rowspan='2'>закон</th><th rowspan='2'>исходные документы в pdf"+refs.makeRef(
			"Наличие ссылок на архивы для скачивания зависит от их доступности на сайте Комитета финансов."
		).ref+"</th><th rowspan='2'>приложение</th><th colspan='3'>данные в машиночитаемом виде"+refData.ref+"</th>")
		w("<tr><th>csv"+refCsv.ref+" без формул</th><th>csv"+refCsv.ref+" с формулами"+refs.makeRef(
			"Для правильной работы формул файл необходимо читать с первой строки."
		).ref+"</th><th>xls</th></tr>\n")
		w("</thead>\n")
		refUnknownSlack=refs.makeRef("Указанные суммы могут расходиться с реальными суммами подпунктов на 100—200 руб. по неизвестным причинам")
		refRoundoffSlack=refs.makeRef(
			"Указанные суммы в графе «Исполнено» могут расходиться с реальными суммами подпунктов из-за округления:"+
			" выплаты производятся с точностью до копейки, а в данном приложении значения указываются с точностью до 100 руб."
		)
		for year,laws in sorted(yearLaws.items()):
			w("<tbody id='"+e(year)+"'>\n");
			w("<tr>")
			wtdrowspan(sum(max(len(law.documents),1) for law in laws),e(year))
			wn=nonFirstWrite()
			for law in laws:
				wn("<tr>")
				wtdrowspan(max(len(law.documents),1),"<span title='"+e(law.title)+"'>"+e(law.description)+"</span>"+
					(refUnknownSlack.ref if any('slack' in doc.quirks for doc in law.documents) else "")+
					(refRoundoffSlack.ref if law.version=='i' else "")
				)
				wtdrowspan(max(len(law.documents),1),a(law.viewUrl,"страница")+
					(" "+a(law.downloadUrl,"архив") if law.isSingleDownload else "")+
					(" "+a(law.zipPath,"копия") if law.isSingleZip and zipCopy else "")
				)
				if not law.documents:
					w("<td colspan='4'>"+e(law.availabilityNote)+"</td>\n")
				wn2=nonFirstWrite()
				for doc in law.documents:
					wn2("<tr>")
					w("<td><span title='"+"Приложение "+e(doc.appendixNumber)+". "+e(doc.title)+"'>")
					if len(doc.forYears)==1:
						w("расходы "+e('-'.join(doc.forYears)))
					else:
						w("план "+e('-'.join(doc.forYears)))
					w("</span></td>")
					def matrix(path):
						w("<td><pre><code>"+
							af(path(1,False),"1.")+"<br />"+
							af(path(2,False),"1.2.")+"   "+af(path(2,True),"1.2.")+"<br />"+
							af(path(3,False),"1.2.3.")+"      "+af(path(3,True),"1.2.3.")+
							("<br /> "+af(path(4,False),"...4.")+"       "+af(path(4,True),"...4.") if doc.maxDepth>=4 else "")+
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
			w("<li>"+ref.body+"</li>\n")
		w(
"""</ol>
</body>
</html>
"""
		)

		file.close()
