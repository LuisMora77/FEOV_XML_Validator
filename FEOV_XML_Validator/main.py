import Validator.XMLValidator
import Validator.AuxiliarFunctions
import Validator.SenderValidations
import re

alphabetRegex = "^[a-zA-Z]+$"


def run(path, xmlType):
    result = Validator.XMLValidator.validateXML(path, xmlType)
    # Verifica si todos los elementos de la lista son True
    print("Result de XML: " + str(result))


def checkString(stringg):
    a = re.match(alphabetRegex, stringg)
    if a:
        print(True)
    else:
        print(False)


if __name__ == '__main__':
    #  Esto hay que hacerlo dinámico según negocio lo quiera usar
    run("//gishared/ServidordeArchivos/Documentos por Area/Factura Electronica/OV/CMER_fmcmOC-00049067_CMER-003350130_Signed_v2.xml", 1)

