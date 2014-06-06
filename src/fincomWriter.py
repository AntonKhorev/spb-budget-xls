import writer

class FincomHtmlWriter(writer.HtmlWriter):
	def getLink(self):
		return 'fincom.html'

	def getTitle(self):
		return "Что можно найти на сайте Комитета финансов"

	def writeContents(self,makeFns):
		w,e,a=makeFns('w,e,a')
		w("<h1>Что можно найти на сайте Комитета финансов</h1>\n")
		w("<p>Информация о бюджете находится в нескольких разделах сайта. Так получилось, что однотипная информация за разные периоды времени может быть в разных разделах.</p>\n")
