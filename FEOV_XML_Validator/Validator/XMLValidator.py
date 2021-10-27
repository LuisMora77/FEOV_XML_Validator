import xml.etree.ElementTree
import xml.etree.ElementTree as ET
import XMLValidator.Validator.AuxiliarFunctions as AuxiliarFunctions
import XMLValidator.Validator.SenderValidations as SenderValidations
import XMLValidator.Validator.ReceiverValidations as ReceiverValidations
import XMLValidator.Validator.HeaderValidations as HeaderValidations
import XMLValidator.Validator.DetailsValidations as DetailsValidations
import XMLValidator.Validator.TotalsValidations as TotalsValidations

OKGREEN = '\033[92m'
namespaces = {'factura': 'https://cdn.comprobanteselectronicos.go.cr/xml-schemas/v4.3/facturaElectronica'} # add more as needed

def readPUXml(path):
    try:
        #tree = ET.parse(path)
        tree = ET.fromstring(path)
        root = ET.fromstring(path) # tree.getroot()
        print("ROOT", root)
        return root
    except:
        print("ERROR")
        return "No se pudo leer el archivo"


def validateXML(path, xmlType: str):
    readResult = readPUXml(path)
    print("readResult", readResult)
    if xmlType == '0':
        return validatePUXml(readResult)
    elif xmlType == '1':
        return validateEInvoiceXml(readResult)
    else:
        return "Se utilizó un tipo inválido de XML"


def validatePUXml(data: xml.etree.ElementTree.Element):

    result = [HeaderValidations.validateHeaderInfo(data),
              SenderValidations.validateSenderInfo(data),
              ReceiverValidations.validateReceiverInfo(data),
              DetailsValidations.validateDetailsInfo(data)]

    flat_list = AuxiliarFunctions.flattenList(result)
    response = all(item == True for item in flat_list)
    if response:
        return "XML válido"
        # return f"{OKGREEN}XML válido"
    else:
        return AuxiliarFunctions.formatErrorMessages(flat_list)


def validateEInvoiceXml(data: xml.etree.ElementTree.Element):

    result = [HeaderValidations.validateHeaderInfo(data),
              SenderValidations.validateSenderInfo(data),
              ReceiverValidations.validateReceiverInfo(data),
              DetailsValidations.validateDetailsInfo(data),
              TotalsValidations.validateTotalsInfo(data)]

    flat_list = AuxiliarFunctions.flattenList(result)
    response = all(item == True for item in flat_list)
    if response:
        return "XML válido"
        #return f"{OKGREEN}XML válido"
    else:
        return AuxiliarFunctions.formatErrorMessages(flat_list)
