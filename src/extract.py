# possible installation for linux:
# sudo apt-get install libpdfbox-java
# or download jar:
# http://pdfbox.apache.org/download.html
# pdfbox usage:
# java -jar pdfbox-app-1.7.1.jar ExtractText -encoding UTF-8 pr-bd-2013-15/pr03-2013-15.pdf
# java -jar pdfbox-app-1.7.1.jar ExtractText -encoding UTF-8 -sort pr-bd-2013-15/pr04-2013-15.pdf

import os.path, glob
import subprocess

def processFile(pdfboxPath,outputDirectory,inputFilename):
	print('extracting text from',inputFilename)
	outputFilename=outputDirectory+'/'+os.path.basename(inputFilename[:-4])+'.txt'
	status=subprocess.call(['java','-jar',pdfboxPath,'ExtractText','-encoding','UTF-8','-sort',inputFilename,outputFilename])
	if status!=0:
		raise Exception('external command failure')

root=os.path.realpath(
	os.path.dirname(os.path.realpath(__file__))+'/..'
)
for filename in glob.glob(root+'/pdf/*.pdf'):
	pdfboxPath=root+'/bin/pdfbox-app-1.8.1.jar'
	processFile(pdfboxPath,root+'/txt',filename)
