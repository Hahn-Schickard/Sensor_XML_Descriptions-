import glob 
import os
from os.path import join

class xmlGetter:
	schemaFile = 'None'
	fileList = 'None'
	filePath = 'None'
	
	def __init__(self):
		## Get XML Schema file
		os.chdir('./tests')
		self.schemaFile = join(os.getcwd(),"LWM2M.xml")
		## Go one directory up
		os.chdir('../ipso-descriptions/')
		self.filePath = os.getcwd()

		self.fileList = [] 

		for file in glob.glob("*.xml"):
			if not file == "ipsoConfig.xml":
				self.fileList.append(join(self.filePath,file))

	def getFiles(self): 
		return self.fileList

	def getPath(self): 
		return self.filePath

	def getSchema(self):
		return self.schemaFile
