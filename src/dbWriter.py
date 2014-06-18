import writer

class DbHtmlWriter(writer.HtmlWriter):
	def getLink(self):
		return 'db.html'

	def getTitle(self):
		return "Структура расходов бюджета Санкт-Петербурга за 2014 год в одной таблице"

	def writeContents(self,makeFns):
		files=[
			('departments.xlsx','Ведомственная структура расходов бюджета Санкт-Петербурга'),
			('sections.xlsx','Функциональная структура расходов бюджета Санкт-Петербурга'),
			('pr-bd-2014-16.sql','База данных'),
			('departments.old.xlsx','Ведомственная структура расходов бюджета Санкт-Петербурга (без 1-й корректировки бюджета)'),
			('sections.old.xlsx','Функциональная структура расходов бюджета Санкт-Петербурга (без 1-й корректировки бюджета)'),
			('pr-bd-2014-16.old.sql','База данных (без 1-й корректировки бюджета)'),
		]
		w,e,a=makeFns('w,e,a')
		w("<h1>Структура расходов бюджета Санкт-Петербурга за 2014 год в одной таблице</h1>\n")
		w('<ul>\n')
		for filename,description in files:
			w('<li>'+a(self.linker.getLink('db/'+filename),filename)+' — '+description+'</li>\n')
		w('</ul>\n')
		w("<p>"+a('https://www.dropbox.com/sh/zgnevck3cij1gm0/AABdfNdrzoimxiWDe_DDPfpCa/db','Ссылка на папку dropbox')+" (на случай, если они поменяют ссылки).</p>\n")
		w("<p>Названия целевых статей даны в виде, соответствующем закону о бюджете (некоторые из них изменились по сравнению с проектом закона).</p>\n")
