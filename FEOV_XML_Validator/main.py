import XMLValidator.Validator.XMLValidator as XMLValidator
import re
from django.db import connections, transaction
from django.core.cache import cache # This is the memcache cache.

alphabetRegex = "^[a-zA-Z]+$"

def run(path, xmlType):
    result = XMLValidator.validateXML(path, xmlType)
    # Verifica si todos los elementos de la lista son True
    print("Result de XML: " + str(result))
    return "Result de XML: " + str(result)

def checkString(string):
    a = re.match(alphabetRegex, string)
    
    if a:
        print(True)
    else:
        print(False)

def runPath(xml, typeEinvoice):
    return run(xml, typeEinvoice)