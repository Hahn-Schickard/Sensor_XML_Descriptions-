## Kudos to Emre for the script ideas! 
# Article found at: https://emredjan.github.io/blog/2017/04/08/validating-xml/

from lxml import etree
from StringIO import StringIO
from os.path import join
import sys
from xmlGetter import xmlGetter
from returnCodes import returnCodes

xmlProvider = xmlGetter()
sensorDefinitions = xmlProvider.getFiles()
schemaDefinition = xmlProvider.getSchema()
returnCode = returnCodes.SUCCESS

badIOFileCount = 0
badSyntaxFileCount = 0
malformatedFileCount = 0

invalidIOFileList = []
badSyntaxXMLList = [] 
badFormatXMLList = []

## Load the schema definition
with open(schemaDefinition, 'r') as schema_file: 
	schema_to_check = schema_file.read()

## Parse schema to memory
xmlschema_doc = etree.parse(StringIO(schema_to_check))
xmlschema = etree.XMLSchema(xmlschema_doc)

for sensorDefinition in sensorDefinitions: 
	## Load xml file
	with open(sensorDefinition, 'r') as xml_file:
    		xml_to_check = xml_file.read()
	# parse xml
	try:
	    doc = etree.parse(StringIO(xml_to_check))

	# check for file IO error
	except IOError:
	    invalidIOFileList.append(sensorDefinition)

	# check for XML syntax errors
	except etree.XMLSyntaxError as err:
	    badSyntaxXMLList.append(sensorDefinition)
	    with open(join('./tests','error.log'), 'a+') as error_log_file:
		error_log_file.write("Error in file: " + sensorDefinition + "\n")
		error_log_file.write(str(err.error_log) + "\n")
	    continue

	# validate against schema
	try:
	    xmlschema.assertValid(doc)

	except etree.DocumentInvalid as err:
	    badFormatXMLList.append(sensorDefinition)
	    with open(join('./tests','error.log'), 'a+') as error_log_file:
		error_log_file.write("Error in file: " + sensorDefinition + "\n")
		error_log_file.write(str(err.error_log) + "\n")
	    continue

	except:
	    returnCode = returnCodes.UNKNOWN
	    continue

if returnCode == returnCodes.SUCCESS : 
	if not invalidIOFileList:
		returnCodes.SUCCESS
	else:
		with open(join('./tests','error.log'), 'a+') as error_log_file:
			error_log_file.write("Files not recognized as an xml:\n")
		returnCodes.INVALID_FILE
		for badFile in invalidIOFileList: 
			error_log_file.write(badFile + "\n")
			badIOFileCount = badIOFileCount + 1

	if not badSyntaxXMLList:
		returnCodes.SUCCESS
	else:
		returnCodes.XML_SYNTAX_ERROR
		for badFile in badSyntaxXMLList: 
			badSyntaxFileCount = badSyntaxFileCount + 1
		
	if not badFormatXMLList: 
		returnCodes.SUCCESS
	else:
		returnCodes.MALFORMATED_XML
		for badFile in badFormatXMLList: 
			malformatedFileCount = malformatedFileCount + 1

print("=========== TEST RESULTS ===========")
print("Not recognized files" +' '*12 +": "  + str(badIOFileCount))
print("Files with bad syntax" +' '*11 + ": "   + str(badSyntaxFileCount))
print("Malformated files" +' '*15 + ": "  + str(malformatedFileCount))

if badIOFileCount > 0 or badSyntaxFileCount > 0 or malformatedFileCount > 0: 
	print("\nCheck ./tests/error.log for more information!")
	exit(1)
else : 
	exit(0)
