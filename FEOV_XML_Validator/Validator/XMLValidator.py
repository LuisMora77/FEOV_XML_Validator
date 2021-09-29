import xml.etree.ElementTree
import xml.etree.ElementTree as ET
import Validator.AuxiliarFunctions
import Validator.SenderValidations
import Validator.ReceiverValidations
import Validator.HeaderValidations
import Validator.DetailsValidations


def readXml(path):
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        return root
    except:
        return "No se pudo leer el archivo"


def validateXML(path, xmlType: int):
    readResult = readXml(path)
    if xmlType == 0:
        return validatePUXml(readResult)
    elif xmlType == 1:
        return "Es un XML de Factura"
    else:
        return "Se utilizó un tipo inválido de XML"


def validatePUXml(data: xml.etree.ElementTree.Element):

    result = [Validator.HeaderValidations.validateHeaderInfo(data),
              Validator.SenderValidations.validateSenderInfo(data),
              Validator.ReceiverValidations.validateReceiverInfo(data),
              Validator.DetailsValidations.validateDetailsInfo(data)]

    flat_list = Validator.AuxiliarFunctions.flattenList(result)
    response = all(item == True for item in flat_list)
    if response:
        return "XML válido"
    else:
        return Validator.AuxiliarFunctions.formatErrorMessages(flat_list)


