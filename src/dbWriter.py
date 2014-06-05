#!/usr/bin/env python3

import main
import writer
from linker import Linker

class DbHtmlWriter(writer.HtmlWriter):
	def writeContents(self,makeFns):
		files=[
			('departments.xlsx','Ведомственная структура расходов бюджета Санкт-Петербурга (до проекта 1-й корректировки включительно)'),
			('sections.xlsx','Функциональная структура расходов бюджета Санкт-Петербурга (до проекта 1-й корректировки включительно)'),
			('pr-bd-2014-16.sql','База данных (до проекта 1-й корректировки включительно)'),
			('departments.old.xlsx','Ведомственная структура расходов бюджета Санкт-Петербурга (без 1-й корректировки бюджета)'),
			('sections.old.xlsx','Функциональная структура расходов бюджета Санкт-Петербурга (без 1-й корректировки бюджета)'),
			('pr-bd-2014-16.old.sql','База данных (без 1-й корректировки бюджета)'),
		]
		w,e,a=makeFns('w,e,a')
		w("<h1>Данные о расходах по ведомствам, разделам, видам и целевым статьям за 2014 год, собранные в одну таблицу</h1>\n")
		w('<ul>\n')
		for filename,description in files:
			w('<li>'+a(linker.getLink('db/'+filename),filename)+' — '+description+'</li>\n')
		w('</ul>\n')
		w("<p>"+a('https://www.dropbox.com/sh/zgnevck3cij1gm0/AABdfNdrzoimxiWDe_DDPfpCa/db','Ссылка на папку dropbox')+" (на случай, если они поменяют ссылки).</p>\n")
		w("<p>Названия целевых статей даны в виде, соответствующем закону о бюджете (некоторые из них изменились по сравнению с проектом закона).</p>\n")

if __name__=='__main__':
	env=main.Environment(main.loadData())
	dir=env.rootPath+'/htm'
	linker=Linker(dir,['sql','xlsx'],'db')
	filename=env.rootPath+'/db.html'
	DbHtmlWriter(linker).write(filename)
