#!/usr/bin/env python3

from linker import Linker
import htmlPage
import content.index,content.db,content.fincom

# TODO put into config
spbBudgetXlsPath='..'

if __name__=='__main__':
	linker=Linker('filelists',{
		'csv':['csv'],
		'xls':['xls'],
		'db':['sql','xlsx'],
	})
	htmlPage.HtmlPage('index.html','Данные бюджета Санкт-Петербурга',content.index.content,linker).write('output/index.html')
	htmlPage.HtmlPage('xls.html','Ведомственная структура расходов бюджета Санкт-Петербурга в csv и xls',htmlPage.importContent(spbBudgetXlsPath+'/index.html'),linker).write('output/xls.html')
	htmlPage.HtmlPage('db.html','БД и таблицы расходов бюджета Санкт-Петербурга из разных источников',content.db.content,linker).write('output/db.html')
	htmlPage.HtmlPage('fincom.html','Что можно найти на сайте Комитета финансов',content.fincom.content,linker).write('output/fincom.html')
