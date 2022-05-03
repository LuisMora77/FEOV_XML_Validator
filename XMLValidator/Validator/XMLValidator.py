import xml.etree.ElementTree
import xml.etree.ElementTree as ET
import XMLValidator.Validator.AuxiliarFunctions as AuxiliarFunctions
import XMLValidator.Validator.SenderValidations as SenderValidations
import XMLValidator.Validator.ReceiverValidations as ReceiverValidations
import XMLValidator.Validator.HeaderValidations as HeaderValidations
import XMLValidator.Validator.DetailsValidations as DetailsValidations
import XMLValidator.Validator.TotalsValidations as TotalsValidations
import XMLValidator.Validator.NCHeaderValidations as NCHeaderValidations
import XMLValidator.Validator.NCSenderValidations as NCSenderValidations
import XMLValidator.Validator.NCReceiverValidations as NCReceiverValidations
import XMLValidator.Validator.NCDetailsValidations as NCDetailsValidations
import XMLValidator.Validator.NCTotalsValidations as NCTotalsValidations
import XMLValidator.Validator.TEHeaderValidations as TEHeaderValidations
import XMLValidator.Validator.TESenderValidations as TESenderValidations
import XMLValidator.Validator.TEDetailsValidations as TEDetailsValidations
import XMLValidator.Validator.TETotalsValidations as TETotalsValidations
import XMLValidator.Validator.FECHeaderValidations as FECHeaderValidations
import XMLValidator.Validator.FECSenderValidations as FECSenderValidations
import XMLValidator.Validator.FECReceiverValidations as FECReceiverValidations
import XMLValidator.Validator.FECDetailsValidations as FECDetailsValidations
import XMLValidator.Validator.FECTotalsValidations as FECTotalsValidations
import XMLValidator.Validator.NDHeaderValidations as NDHeaderValidations
import XMLValidator.Validator.NDSenderValidations as NDSenderValidations
import XMLValidator.Validator.NDReceiverValidations as NDReceiverValidations
import XMLValidator.Validator.NDDetailsValidations as NDDetailsValidations
import XMLValidator.Validator.NDTotalsValidations as NDTotalsValidations
import XMLValidator.Validator.FEEHeaderValidations as FEEHeaderValidations
import XMLValidator.Validator.FEESenderValidations as FEESenderValidations
import XMLValidator.Validator.FEEReceiverValidations as FEEReceiverValidations
import XMLValidator.Validator.FEEDetailsValidations as FEEDetailsValidations
import XMLValidator.Validator.FEETotalsValidations as FEETotalsValidations
import XMLValidator.Validator.referenceinformation as ReferenceInformation
import XMLValidator.Validator.NDreferenceinformation as NDReferenceInformation


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


def validateXML(path, xmlType: str, docType: str):
    readResult = readPUXml(path)
    print("readResult", readResult)
    if xmlType == '0':
        if docType =='01':
            return validatePUXml(readResult)
        if docType =='02':
            return validateNDXml(readResult)
        if docType == '03':
            return validateNCXml(readResult)
        if docType == '04':
            return validateTEXml(readResult)
        if docType == '08':
            return validateFECXml(readResult)
        if docType == '09':
            return validateFEEXml(readResult)
    elif xmlType == '1':
        if docType =='01':
            return validateEInvoiceXml(readResult)
        if docType =='02':
            return validateEInvoiceNDXml(readResult)
        if docType == '03':
            return validateEInvoiceNCXml(readResult)
        if docType == '04':
            return validateEInvoiceTEXml(readResult)
        if docType == '08':
            return validateEInvoiceFECXml(readResult)
        if docType == '09':
            return validateEInvoiceFEEXml(readResult)
        
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

def validateNCXml(data: xml.etree.ElementTree.Element):

    result = [NCHeaderValidations.validateHeaderInfo(data),
              NCSenderValidations.validateSenderInfo(data),
              NCReceiverValidations.validateReceiverInfo(data),
              NCDetailsValidations.validateDetailsInfo(data),
              NCTotalsValidations.validateTotalsInfo(data),
              ReferenceInformation.validateReferenceInfo(data)]

    flat_list = AuxiliarFunctions.flattenList(result)
    response = all(item == True for item in flat_list)
    if response:
        return "XML válido"
        # return f"{OKGREEN}XML válido"
    else:
        return AuxiliarFunctions.formatErrorMessages(flat_list)

def validateTEXml(data: xml.etree.ElementTree.Element):

    result = [TEHeaderValidations.validateHeaderInfo(data),
              TESenderValidations.validateSenderInfo(data),
              TETotalsValidations.validateTotalsInfo(data),
              TEDetailsValidations.validateDetailsInfo(data)]

    flat_list = AuxiliarFunctions.flattenList(result)
    response = all(item == True for item in flat_list)
    if response:
        return "XML válido"
        # return f"{OKGREEN}XML válido"
    else:
        return AuxiliarFunctions.formatErrorMessages(flat_list)


def validateFECXml(data: xml.etree.ElementTree.Element):

    result = [FECHeaderValidations.validateHeaderInfo(data),
              FECSenderValidations.validateSenderInfo(data),
              FECReceiverValidations.validateReceiverInfo(data),
              FECTotalsValidations.validateTotalsInfo(data),
              FECDetailsValidations.validateDetailsInfo(data)]

    flat_list = AuxiliarFunctions.flattenList(result)
    response = all(item == True for item in flat_list)
    if response:
        return "XML válido"
        # return f"{OKGREEN}XML válido"
    else:
        return AuxiliarFunctions.formatErrorMessages(flat_list)

def validateNDXml(data: xml.etree.ElementTree.Element):

    result = [NDHeaderValidations.validateHeaderInfo(data),
              NDSenderValidations.validateSenderInfo(data),
              NDReceiverValidations.validateReceiverInfo(data),
              NDTotalsValidations.validateTotalsInfo(data),
              NDDetailsValidations.validateDetailsInfo(data),
              NDReferenceInformation.validateReferenceInfo(data)]

    flat_list = AuxiliarFunctions.flattenList(result)
    response = all(item == True for item in flat_list)
    if response:
        return "XML válido"
        # return f"{OKGREEN}XML válido"
    else:
        return AuxiliarFunctions.formatErrorMessages(flat_list)

def validateFEEXml(data: xml.etree.ElementTree.Element):

    result = [FEEHeaderValidations.validateHeaderInfo(data),
              FEESenderValidations.validateSenderInfo(data),
              FEEReceiverValidations.validateReceiverInfo(data),
              FEETotalsValidations.validateTotalsInfo(data),
              FEEDetailsValidations.validateDetailsInfo(data)]

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


def validateEInvoiceNCXml(data: xml.etree.ElementTree.Element):

 #return "Entro al NC Validate"

    result = [NCHeaderValidations.validateHeaderInfo(data),
              NCSenderValidations.validateSenderInfo(data),
              NCReceiverValidations.validateReceiverInfo(data),
              NCDetailsValidations.validateDetailsInfo(data),
              NCTotalsValidations.validateTotalsInfo(data),
              ReferenceInformation.validateReferenceInfo(data)]
    flat_list = AuxiliarFunctions.flattenList(result)
    response = all(item == True for item in flat_list)
    if response:
        return "XML válido"
        #return f"{OKGREEN}XML válido"
    else:
        return AuxiliarFunctions.formatErrorMessages(flat_list)


def validateEInvoiceTEXml(data: xml.etree.ElementTree.Element):

    #return "Entro al TE Validate"
    result = [TEHeaderValidations.validateHeaderInfo(data),
              TESenderValidations.validateSenderInfo(data),
              TEDetailsValidations.validateDetailsInfo(data),
              TETotalsValidations.validateTotalsInfo(data)]

    flat_list = AuxiliarFunctions.flattenList(result)
    response = all(item == True for item in flat_list)
    if response:
        return "XML válido"
        #return f"{OKGREEN}XML válido"
    else:
        return AuxiliarFunctions.formatErrorMessages(flat_list)


def validateEInvoiceFECXml(data: xml.etree.ElementTree.Element):

    #return "Entro al TE Validate"
    result = [FECHeaderValidations.validateHeaderInfo(data),
              FECSenderValidations.validateSenderInfo(data),
              FECReceiverValidations.validateReceiverInfo(data),
              FECTotalsValidations.validateTotalsInfo(data),
              FECDetailsValidations.validateDetailsInfo(data)]

    flat_list = AuxiliarFunctions.flattenList(result)
    response = all(item == True for item in flat_list)
    if response:
        return "XML válido"
        #return f"{OKGREEN}XML válido"
    else:
        return AuxiliarFunctions.formatErrorMessages(flat_list)

def validateEInvoiceNDXml(data: xml.etree.ElementTree.Element):

    #return "Entro al TE Validate"
    result = [NDHeaderValidations.validateHeaderInfo(data),
              NDSenderValidations.validateSenderInfo(data),
              NDReceiverValidations.validateReceiverInfo(data),
              NDTotalsValidations.validateTotalsInfo(data),
              NDDetailsValidations.validateDetailsInfo(data),
              NDReferenceInformation.validateReferenceInfo(data)]

    flat_list = AuxiliarFunctions.flattenList(result)
    response = all(item == True for item in flat_list)
    if response:
        return "XML válido"
        #return f"{OKGREEN}XML válido"
    else:
        return AuxiliarFunctions.formatErrorMessages(flat_list)

def validateEInvoiceFEEXml(data: xml.etree.ElementTree.Element):

    #return "Entro al TE Validate"
    result = [FEEHeaderValidations.validateHeaderInfo(data),
              FEESenderValidations.validateSenderInfo(data),
              FEEReceiverValidations.validateReceiverInfo(data),
              FEETotalsValidations.validateTotalsInfo(data),
              FEEDetailsValidations.validateDetailsInfo(data)]

    flat_list = AuxiliarFunctions.flattenList(result)
    response = all(item == True for item in flat_list)
    if response:
        return "XML válido"
        #return f"{OKGREEN}XML válido"
    else:
        return AuxiliarFunctions.formatErrorMessages(flat_list)