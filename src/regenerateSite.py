#!/usr/bin/env python3

import main,linker,dbWriter

if __name__=='__main__':
	env=main.Environment(main.loadData())
	dir=env.rootPath+'/htm'
	indexLinker=linker.Linker(dir,['csv','xls'])
	env.writeHtml(indexLinker) # index.html
	dbLinker=linker.Linker(dir,['sql','xlsx'],'db')
	dbWriter.DbHtmlWriter(dbLinker).write(env.rootPath+'/db.html') # db.html
