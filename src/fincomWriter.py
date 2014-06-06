import writer

class FincomHtmlWriter(writer.HtmlWriter):
	def getLink(self):
		return 'fincom.html'

	def getTitle(self):
		return "Что можно найти на сайте Комитета финансов"

	def writeContents(self,makeFns):
		w,wtd,e,a=makeFns('w,wtd,e,a')
		w("<h1>Что можно найти на сайте Комитета финансов</h1>\n")
		w("<p>Информация о бюджете находится в нескольких разделах сайта. Так получилось, что однотипная информация за разные периоды времени может быть в разных разделах.</p>\n")
		def aZipPdf(link):
			return a(link,'[zip]',title='zip-архив с pdf-документом')
		def aHtmlDropdownNav(link):
			return a(link,'[html]',title='несколько html-страниц с навигацией в виде выпадающего списка')
		w("<table>\n")
		w("<thead>\n")
		w("<tr><th>год</th><th>губернатор</th><th title='публикации «Бюджет в кратком изложении» и «Бюджет для граждан» объёмом 60—80 страниц'>презентация</th></tr>\n")
		w("</thead>\n")
		w("<tbody id='2000'><tr>")
		wtd("2000")
		wtd("Яковлев")
		wtd(aZipPdf('http://www.fincom.spb.ru/files/cf/presentations/budg00_l.zip'))
		w("</tr></tbody>\n")
		w("<tbody id='2001'><tr>")
		wtd("2001")
		wtd("Яковлев")
		wtd(aZipPdf('http://www.fincom.spb.ru/files/cf/presentations/bl_01.zip'))
		w("</tr></tbody>\n")
		w("<tbody id='2002'><tr>")
		wtd("2002")
		wtd("Яковлев")
		wtd()
		w("</tr></tbody>\n")
		w("<tbody id='2003'><tr>")
		wtd("2003")
		wtd("Яковлев")
		wtd(aZipPdf('http://www.fincom.spb.ru/files/cf/presentations/bl-03.zip'))
		w("</tr></tbody>\n")
		w("<tbody id='2004'><tr>")
		wtd("2004")
		wtd("Матвиенко")
		wtd(aZipPdf('http://www.fincom.spb.ru/files/cf/presentations/bl_04.zip'))
		w("</tr></tbody>\n")
		w("<tbody id='2005'><tr>")
		wtd("2005")
		wtd("Матвиенко")
		wtd(aZipPdf('http://www.fincom.spb.ru/files/cf/presentations/bl_05.zip')+' '+aHtmlDropdownNav('http://www.fincom.spb.ru/files/cf/presentations_html/Budjet_2005_short/bd2005.html'))
		w("</tr></tbody>\n")
		w("</table>\n")
