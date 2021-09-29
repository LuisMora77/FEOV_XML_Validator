import Validator.XMLValidator
import Validator.AuxiliarFunctions
import Validator.SenderValidations
import re
def run(path, xmlType):
    result = Validator.XMLValidator.validateXML(path, xmlType)
    # Verifica si todos los elementos de la lista son True
    print("Result de XML: " + str(result))


#cmer_OV_01780379
#a = Validator.AuxiliarFunctions.validateDecimal("12345678901235171.137", 17, 3)
#print(a)
#run("//gishared/ServidordeArchivos/Documentos por Area/Factura Electronica/OV/cmer_OV_01778539.xml", 0)
#run("//gishared/ServidordeArchivos/Documentos por Area/Factura Electronica/OV/cmer_OV_01780379.xml", 0)
# print(Validator.AuxiliarFunctions.isValidDateTime("2021-09-15 04:11:50"))
REEmailSender = "^\\s*(([^<>()\\[\\]\\.,;:\\s@\\\"]+(\\.[^<>()\\[\\]\\.,;:\\s@\\\"]+)*)|(\\\".+\\\"))@(([^<>()\\[\\]\\.,;:\\s@\\\"]+\\.)+[^<>()\\[\\]\\.,;:\\s@\\\"]{0,})\\s*$"
variable = "fe@grupointeca.com"



if __name__ == '__main__':
    run("//gishared/ServidordeArchivos/Documentos por Area/Factura Electronica/OV/cmer_OV_01778539.xml", 0)

def check():
    if re.match(REEmailSender, variable):
        print("True")
    else:
        print("False")

#check()
