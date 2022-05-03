import datetime
from dateutil.parser import parse
import xml.etree.ElementTree
import XMLValidator.Validator.AuxiliarFunctions as AuxiliarFunctions

namespaces = {'eInvoiceNameSpace': 'https://cdn.comprobanteselectronicos.go.cr/xml-schemas/v4.3/notaCreditoElectronica'} # add more as needed

def prependNamespace(node):
    return '{https://cdn.comprobanteselectronicos.go.cr/xml-schemas/v4.3/notaCreditoElectronica}' + node


def validateReferenceInfo(data: xml.etree.ElementTree.Element):
    senderReferenceinfoNode = data.find('eInvoiceNameSpace:InformacionReferencia', namespaces)
    results = [validateReferenceInfoNode(senderReferenceinfoNode),validateDocumentType(senderReferenceinfoNode),
    validatReferenceCode(senderReferenceinfoNode),validateSentDate(senderReferenceinfoNode),validateReasonEmpty(senderReferenceinfoNode)]
    formattedHeaderResults = AuxiliarFunctions.flattenList(results)
    return formattedHeaderResults

def validateReferenceInfoNode(senderReferenceinfoNode):
    if senderReferenceinfoNode:
        return True
    else:
        return "No existe Nodo de InformacionReferencia en el XML"

def validatReferenceCode(senderReferenceinfoNode):
   
        try:
            docType = senderReferenceinfoNode.find('eInvoiceNameSpace:TipoDoc', namespaces).text
            if docType != "99" and docType != "13":
                    number = senderReferenceinfoNode.find('eInvoiceNameSpace:Numero', namespaces).text
                    if len(number) == 0 or len(number) != 50:
                        return "-25, La calve de referencia no puede estar vacío ni exceder, ni ser minimo los 50 caracteres, en la sección './/InformacionReferencia"
                    else:
                        return True
            else:
                return True
        except:
            return "Nodo 'Numero' de sección de Informacion de referencia no puede ser vacío,en la sección './/InformacionReferencia"


def validateDocumentType(senderReferenceinfoNode):
    try:
        docType = senderReferenceinfoNode.find('eInvoiceNameSpace:TipoDoc', namespaces).text
        if len(docType) != 2:
            return "TipoDoc (" + docType + ") posee un número de dígitos no permitido, debe ser igual a (2), en la sección './/InformacionReferencia"
        else:
            return True
    except:
        return "Nodo 'TipoDoc' no puede ser vacío."

def validateDocumentType(senderReferenceinfoNode):
    try:
        acceptedConditions = ["01", "02", "03", "04", "05", "06", "07", "08", "09","13","99"]  # 
        salesConditionNode = senderReferenceinfoNode.find('eInvoiceNameSpace:TipoDoc', namespaces).text
        if len(salesConditionNode) != 2 or salesConditionNode not in acceptedConditions:
            return "El valor (" + salesConditionNode + ") del nodo 'TipoDoc' en la sección del encabezado," \
                                                   " no es válido con respecto al catálogo de tipos: " + str(
            acceptedConditions)
        else:
            return True
    except:
        return "Nodo 'TipoDoc' en sección de //InformacionReferencia no puede ser vacío."


def validateCode(senderReferenceinfoNode):
        try:
            docType = senderReferenceinfoNode.find('eInvoiceNameSpace:TipoDoc', namespaces).text
            if docType != "13":
                code = senderReferenceinfoNode.find('eInvoiceNameSpace:Codigo', namespaces).text
                if len(code) != 2:
                    return "Codigo (" + code + ") posee un número de dígitos no permitido, debe ser igual a (2) en sección './/InformacionReferencia"
                else:
                    return True
            else: 
                return True
        except:
            return "Nodo 'Codigo' no puede ser vacío, en sección './/InformacionReferencia"

def isValidDateTime(dateTimeStr):
    try:
        parse(dateTimeStr)
        return True
    except ValueError:
        return False


def manageDateTimeFormatValidation(dateTimeStr):
    isValid = isValidDateTime(dateTimeStr)
    if isValid == False:
        return "Error -1, No es un formato de fecha válido, en sección './/InformacionReferencia"
    else:
        return True

    # Retorna True si date1 es mayor que date2


def isValidDateSpan(date1, date2) -> bool:
    now = parse(date1)
    sentDate = parse(date2)
    return True if (now > sentDate) else False


def manageDateSpanValidation(sentDate):
    isValidSpan = isValidDateSpan(str(datetime.datetime.now()), sentDate)
    if isValidSpan == False:
        return "Error -53 : La fecha de emisión del comprobante no puede ser superior al día de hoy, en sección './/InformacionReferencia"
    else:
        return True


def validateSentDate(senderReferenceinfoNode):
    try:
        dateStr = senderReferenceinfoNode.find('eInvoiceNameSpace:FechaEmision', namespaces).text
        results = [manageDateTimeFormatValidation(dateStr), manageDateSpanValidation(dateStr)]
        return results
    except:
        return "Nodo 'FechaEmision' no puede ser vacío, en sección './/InformacionReferencia"



def validateReasonEmpty(senderReferenceinfoNode):
  
        try:
            docType = senderReferenceinfoNode.find('eInvoiceNameSpace:TipoDoc', namespaces).text
            if docType != "13":
                Reason = senderReferenceinfoNode.find('eInvoiceNameSpace:Razon', namespaces).text
                if len(Reason) == 0 or len(Reason) > 180:
                    return "-25, El nombre de Razon no puede estar vacío ni exceder los 180 caracteres"
                else:
                    return True
            else:
                return True
        except:
            return "Nodo 'Razon' de sección de Informacion de referencia no puede ser vacío "


