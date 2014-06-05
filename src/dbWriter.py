#!/usr/bin/env python3

import main
import writer
from linker import Linker

class DbHtmlWriter(writer.HtmlWriter):
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
		w('<ul>')
		for filename,description in files:
			w('<li>'+a(linker.getLink('db/'+filename),filename)+' — '+description+'</li>')
		w('</ul>')
		w("<p>Названия целевых статей даны в виде, соответствующем закону о бюджете (некоторые из них изменились по сравнению с проектом закона).</p>")

if __name__=='__main__':
	env=main.Environment(main.loadData())
	dir=env.rootPath+'/htm'
	linker=Linker(dir,['sql','xlsx'],'db')
	filename=env.rootPath+'/db.html'
	DbHtmlWriter(linker).write(filename)
