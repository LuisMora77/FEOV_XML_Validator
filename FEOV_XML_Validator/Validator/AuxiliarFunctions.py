import re

REOnlyNumbers = "[0-9]+$"  # Expresion regular que solo acepta números


def validatePhysicalID(id):
    if id[0] == "0" or len(id) != 9 or ("-" in id):
        return "La cedula fisica del emisor (" + str(id) + ") no posee la estructura adecuada"
    else:
        return True


def validateLegalID(id):
    if len(id) != 10 or ("-" in id):
        return "La cedula juridica del emisor (" + str(id) + ") no posee la estructura adecuada"
    else:
        return True


def validateDIMEXID(id):
    if id[0] == "0" or len(id) not in [11, 12] or ("-" in id):
        return "La cedula DIMEX del emisor (" + str(id) + ") no posee la estructura adecuada"
    else:
        return True


def validateNITEID(id):
    if len(id) != 10 or ("-" in id):
        return "La cedula NITE del emisor (" + str(id) + ") no posee la estructura adecuada"
    else:
        return True


def flattenList(lista):
    flatList = []
    for i in lista:
        if isinstance(i, list):
            for j in i:
                flatList.append(j)
        else:
            flatList.append(i)
    return flatList


def formatErrorMessages(lista):
    errorsString = ""
    for i in lista:
        if isinstance(i, str):
            errorsString += "- " + i + " \n"
    return "El XML posee los siguentes errores: " + "\n" + errorsString


# Valida formato de decimales según parámetros
# numberStr: String de número decimal
# wholeNumbers: Cantidad máxima de valores enteros aceptados
# decimals: Cantidad de decimales requerida
def validateDecimal(numberStr, wholeNumbers, decimals):
    numbers = numberStr.replace(".", "")
    totalDecimals = numberStr[::-1].find(".")
    totalwholeNumbers = numberStr.find(".")
    if re.match(REOnlyNumbers, numbers) is not None and totalDecimals == decimals and totalwholeNumbers <= wholeNumbers:
        return True
    else:
        return False
