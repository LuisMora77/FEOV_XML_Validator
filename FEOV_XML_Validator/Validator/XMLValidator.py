import xml.etree.ElementTree
import xml.etree.ElementTree as ET
import Validator.AuxiliarFunctions
import Validator.SenderValidations
import Validator.ReceiverValidations
import Validator.HeaderValidations
import Validator.DetailsValidations
import Validator.TotalsValidations

OKGREEN = '\033[92m'
namespaces = {'factura': 'https://cdn.comprobanteselectronicos.go.cr/xml-schemas/v4.3/facturaElectronica'} # add more as needed


def readPUXml(path):
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        return root
    except:
        return "No se pudo leer el archivo"

def prepend_ns(s):
    return '{https://cdn.comprobanteselectronicos.go.cr/xml-schemas/v4.3/facturaElectronica}' + s


def validateXML(path, xmlType: int):
    readResult = readPUXml(path)
    if xmlType == 0:
        return validatePUXml(readResult)
    elif xmlType == 1:
        #readResult = readEInvoiceXml(path)
        #return validateEInvoiceXml(readResult)
        return "a"
    else:
        return "Se utilizó un tipo inválido de XML"


def validatePUXml(data: xml.etree.ElementTree.Element):

    result = [Validator.HeaderValidations.validateHeaderInfo(data),
              Validator.SenderValidations.validateSenderInfo(data),
              Validator.ReceiverValidations.validateReceiverInfo(data),
              Validator.DetailsValidations.validateDetailsInfo(data),
              Validator.TotalsValidations.validateTotalsInfo(data)]

    flat_list = Validator.AuxiliarFunctions.flattenList(result)
    response = all(item == True for item in flat_list)
    #print("Results: " + str(flat_list))
    if response:
        return f"{OKGREEN}XML válido"
    else:
        return Validator.AuxiliarFunctions.formatErrorMessages(flat_list)


