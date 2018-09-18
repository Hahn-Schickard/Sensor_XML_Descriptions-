from enum import Enum

class returnCodes(Enum): 
	SUCCESS = 0
	INVALID_FILE = 1
	XML_SYNTAX_ERROR = 2
	MALFORMATED_XML = 3
	UNKNOWN = 4
	
