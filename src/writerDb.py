#!/usr/bin/env python3

import html

import main
from linker import Linker

if __name__=='__main__':
	env=main.Environment(main.loadData())
	dir=env.rootPath+'/htm'
	linker=Linker(dir,['sql','xlsx'],'db')
	files=[
		('departments.xlsx','Ведомственная структура расходов бюджета Санкт-Петербурга'),
		('sections.xlsx','Функциональная структура расходов бюджета Санкт-Петербурга'),
		('pr-bd-2014-16.sql','База данных'),
		('departments.old.xlsx','Ведомственная структура расходов бюджета Санкт-Петербурга (без 1-й корректировки бюджета)'),
		('sections.old.xlsx','Функциональная структура расходов бюджета Санкт-Петербурга (без 1-й корректировки бюджета)'),
		('pr-bd-2014-16.old.sql','База данных (без 1-й корректировки бюджета)'),
	]
	filename=env.rootPath+'/db.html'
	with open(filename,'w',encoding='utf-8') as file:
		w=file.write
		e=lambda x: html.escape(str(x))
		a=lambda link,text: "<a href='"+e(link)+"'>"+text+"</a>"
		w("<html><head><meta charset='utf-8'></head><body>")
		w('<ul>')
		for filename,description in files:
			w('<li>'+a(linker.getLink('db/'+filename),filename)+' — '+description+'</li>')
		w('</ul>')
		w("<p>Названия целевых статей даны в виде, соответствующем закону о бюджете (некоторые из них изменились по сравнению с проектом закона).</p>")
		w("</body></html>")
