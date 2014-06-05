import collections

import writer

class IndexHtmlWriter(writer.HtmlWriter):
	def __init__(self,linker,env):
		super().__init__(linker)
		self.env=env

	def writeContents(self,makeFns):
		w,nonFirstWrite,wtd,wtdrowspan,e,a,af=makeFns('w,nonFirstWrite,wtd,wtdrowspan,e,a,af')

		refs=writer.HtmlWriter.Refs()
		w("<h1>Ведомственная структура расходов бюджета Санкт-Петербурга</h1>\n")

		abbrXls="<abbr title='Excel Binary File Format, бинарный формат файлов Excel'>xls</abbr>"
		abbrPdf="<abbr title='Portable Document Format'>pdf</abbr>"
		abbrCsv="<abbr title='comma-separated values, значения, разделённые запятыми'>csv</abbr>"
		abbrUtf8="<abbr title='Unicode Transformation Format, 8-bit'>utf-8</abbr>"

		w("<p>Последнее обновление: 04.06.2014."+refs.makeRef(
			"<dl>"
			"<dt>31.05.2013</dt><dd>Добавлен закон 1-й корректировки бюджета 2013 г. и закон об исполнении бюджета 2011 г.</dd>"
			"<dt>04.06.2013</dt><dd>Добавлены законы 2009—2010 гг.</dd>"
			"<dt>24.08.2013</dt><dd>Добавлены законы 2008 г., кроме небольших корректировок расходов.</dd>"
			"<dt>26.08.2013</dt><dd>Добавлены законы 2000—2007 г., многие из которых оказались уже доступными в формате "+abbrXls+".</dd>"
			"<dt>04.10.2013</dt><dd>Добавлен проект закона о бюджете на 2014 г.</dd>"
			"<dt>20.04.2014</dt><dd>Добавлен закон 2014 г. и проект его 1-й корректировки.</dd>"
			"<dt>21.04.2014</dt><dd>В проекте 1-й корректировки 2014 г. добавлен код Комитета по межнациональным отношениям.</dd>"
			"<dt>04.06.2014</dt><dd>Добавлен закон 1-й корректировки бюджета 2014 г.</dd>"
			"</dl>"
		).ref+"</p>\n")

		yearLaws=collections.defaultdict(list)
		yearExtracted=collections.defaultdict(bool)
		for law in self.env.laws:
			yearLaws[law.year].append(law)
			if law.documents:
				yearExtracted[law.year]=True
		w("<p>Документы для годов: ")
		wn=nonFirstWrite()
		for year in sorted(yearLaws):
			wn(", ")
			w(a("#"+year,e(year)))
		w(".</p>\n")

		w("<p>Для 2014 г. также доступен "+a("db.html","вариант со всеми поправками, собранными в одну таблицу")+".</p>\n")

		w("<h2>Данные, для которых извлечение не производилось</h2>\n")
		w(
			"<p>До 2007 года "+a("http://www.fincom.spb.ru/","Комитет финансов Санкт-Петербурга")+" публиковал таблицы из приложений к бюджету в формате "+abbrXls+". "
			"Таблицы можно найти на сайте комитета в разделе "+a("http://www.fincom.spb.ru/comfin/budjet/laws.htm","«Законы о бюджете»")+". "
			"Позже в этом формате в разделе "+a("http://www.fincom.spb.ru/comfin/budjet/budget_for_people.htm","«Бюджет для граждан»")+" был опубликован проект закона и закон о бюджете на 2014 год.</p>\n"
		)
		w("<table>\n")
		w("<thead>\n")
		w("<tr><th>год</th><th>закон</th><th>исходные документы</th><th>данные в машиночитаемом виде</th></tr>\n")
		w("</thead>\n")
		for year,laws in sorted(yearLaws.items()):
			if yearExtracted[year]:
				continue
			w("<tbody id='"+e(year)+"'>\n");
			w("<tr>")
			wtdrowspan(sum(max(len(law.documents),1) for law in laws),e(year))
			wn=nonFirstWrite()
			for law in laws:
				wn("<tr>")
				wtd("<span title='"+e(law.title)+"'>"+e(law.description)+"</span>")
				wtd(a(law.viewUrl,"страница")+
					(" "+a(law.downloadUrl,"архив") if law.isSingleDownload else "")+
					(" "+a(law.zipPath,"копия") if law.isSingleZip and not self.isExternal else "")
				)
				if law.originalXlsUrl is not None:
					wtd(a(law.originalXlsUrl,e(law.availabilityNote)))
				else:
					wtd(e(law.availabilityNote))
				w("</tr>\n")
			w("</tbody>\n");
		w("</table>\n")

		w("<h2>Извлечённые данные</h2>\n")
		w("<p>С 2007 года приложения к законам о бюджете публикуются в формате "+abbrPdf+". Работать с таблицами в этом формате может быть неудобно. Ниже приводятся данные, автоматически"+refs.makeRef(
			a("https://github.com/AntonKhorev/BudgetSpb","Исходный код программы для извлечения")+"."
		).ref+" извлечённые из приложений.</p>\n")
		refData=refs.makeRef(
			"<pre><code>"
			"1.                  \<br />"
			"1.2.   1.2.          ) разные уровни раскрытия<br />"
			"1.2.3.      1.2.3.  /<br />"
			"  |             \<br />"
			"«столбиком»   «лесенкой» — в этом варианте проще формулы для суммирования"
			"</code></pre>"
		)
		refCsv=refs.makeRef("В кодировке "+abbrUtf8+". Числа с десятичной запятой, потому что в таком формате их читают русские версии электронных таблиц.")
		w("<table>\n")
		w("<thead>\n")
		w("<tr><th rowspan='2'>год</th><th rowspan='2'>закон</th><th rowspan='2'>исходные документы"+refs.makeRef(
			"Наличие ссылок на архивы для скачивания зависит от их доступности на сайте Комитета финансов."
		).ref+"</th><th rowspan='2'>приложение</th><th colspan='3'>данные в машиночитаемом виде"+refData.ref+"</th></tr>\n")
		w("<tr><th>"+abbrCsv+refCsv.ref+" без формул</th><th>"+abbrCsv+refCsv.ref+" с формулами"+refs.makeRef(
			"Для правильной работы формул файл необходимо читать с первой строки."
		).ref+"</th><th>"+abbrXls+"</th></tr>\n")
		w("</thead>\n")
		refUnknownSlack=refs.makeRef("Указанные суммы могут расходиться с реальными суммами подпунктов на 100—200 руб. по неизвестным причинам.")
		refRoundoffSlack=refs.makeRef(
			"Указанные суммы в графе «Исполнено» могут расходиться с реальными суммами подпунктов из-за округления:"+
			" выплаты производятся с точностью до копейки, а в данном приложении значения указываются с точностью до 100 руб."
		)
		for year,laws in sorted(yearLaws.items()):
			if not yearExtracted[year]:
				continue
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
					(" "+a(law.zipPath,"копия") if law.isSingleZip and not self.isExternal else "")
				)
				if not law.documents:
					if law.originalXlsUrl is not None:
						w("<td colspan='4'>"+a(law.originalXlsUrl,e(law.availabilityNote))+"</td>")
					else:
						w("<td colspan='4'>"+e(law.availabilityNote)+"</td>")
					w("</tr>\n")
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

		w("<h2>Примечания</h2>\n<ol>\n")
		for ref in refs:
			w("<li>"+ref.body+"</li>\n")
		w("</ol>\n")
