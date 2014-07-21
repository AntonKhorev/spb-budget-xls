#!/usr/bin/env python3

import main,linker,dbWriter,fincomWriter

if __name__=='__main__':
	env=main.Environment(main.loadData())
	dir=env.rootPath+'/htm'
	linker=linker.Linker(env.rootPath+'/htm',{
		'csv':['csv'],
		'xls':['xls'],
		'db':['sql','xlsx'],
	})
	env.writeHtml(linker) # xls.html
	dbWriter.DbHtmlWriter(linker).write(env.rootPath+'/db.html') # db.html
	fincomWriter.FincomHtmlWriter(linker).write(env.rootPath+'/fincom.html') # fincom.html
