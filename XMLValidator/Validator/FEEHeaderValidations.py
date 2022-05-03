import datetime
from dateutil.parser import parse
import xml.etree.ElementTree
import XMLValidator.Validator.AuxiliarFunctions as AuxiliarFunctions

namespaces = {'eInvoiceNameSpace': 'https://cdn.comprobanteselectronicos.go.cr/xml-schemas/v4.3/facturaElectronicaExportacion'} # add more as needed

def prependNamespace(node):
    return '{https://cdn.comprobanteselectronicos.go.cr/xml-schemas/v4.3/facturaElectronicaExportacion}' + node


def validateHeaderInfo(data: xml.etree.ElementTree.Element):

    results = [validateActivityCode(data), validateSentDate(data), validateSalesCondition(data),
               validateSalesConditionNumber(data), validateSalesCreditTerm(data),
               validateSalesCeditTermFormat(data), validatePaymentMethod(data), validatePaymentMethodFormat(data)]
    formattedHeaderResults = AuxiliarFunctions.flattenList(results)
    return formattedHeaderResults

def validateActivityCode(data: xml.etree.ElementTree.Element):
    try:
        code = data.find('eInvoiceNameSpace:CodigoActividad', namespaces).text
        if len(code) > 6:
            return "Código de actividad (" + code + ") posee un número de dígitos mayor al permitido (6)"
        else:
            return True
    except:
        return "Nodo 'CodigoActividad' no puede ser vacío."


def isValidDateTime(dateTimeStr):
    try:
        parse(dateTimeStr)
        return True
    except ValueError:
        return False


def manageDateTimeFormatValidation(dateTimeStr):
    isValid = isValidDateTime(dateTimeStr)
    if isValid == False:
        return "Error -1, No es un formato de fecha válido"
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
        return "Error -53 : La fecha de emisión del comprobante no puede ser superior al día de hoy"
    else:
        return True


def validateSentDate(data: xml.etree.ElementTree.Element):
    try:
        dateStr = data.find('eInvoiceNameSpace:FechaEmision', namespaces).text
        results = [manageDateTimeFormatValidation(dateStr), manageDateSpanValidation(dateStr)]
        return results
    except:
        return "Nodo 'FechaEmision' en sección de encabezado no puede ser vacío."

def validateSalesCondition(data: xml.etree.ElementTree.Element):
    ConditionNode = data.findall('eInvoiceNameSpace:CondicionVenta', namespaces)
    if len(ConditionNode) == 0:
        return "No se encuenta nodo de Condición de venta, el cual es de caracter obligatorio."
    else:
        return True

def validateSalesConditionNumber(data: xml.etree.ElementTree.Element):
    try:
        acceptedConditions = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "99"]  # 02 = Crédito
        salesConditionNode = data.find('eInvoiceNameSpace:CondicionVenta', namespaces).text
        if len(salesConditionNode) != 2 or salesConditionNode not in acceptedConditions:
            return "El valor (" + salesConditionNode + ") del nodo 'CondicionVenta' en la sección del encabezado," \
                                                   " no es válido con respecto al catálogo de tipos: " + str(
            acceptedConditions)
        else:
            return True
    except:
        return "Nodo 'CondicionVenta' en sección de encabezado no puede ser vacío."


def validateSalesCreditTerm(data: xml.etree.ElementTree.Element):
    try:
        salesConditionNode = data.find('eInvoiceNameSpace:CondicionVenta', namespaces).text
    except:
        return "No existe nodo 'CondicionVenta', por lo que no se puede evaluar el plazo de crédito."
    if salesConditionNode == "02":
        CreditTermNode = data.findall('eInvoiceNameSpace:PlazoCredito', namespaces)
        if len(CreditTermNode) == 0:
            return "No existe Nodo de Plazo de credito en encabezado, el cual es de caracter obligatoeio"
        else:
            return True
    else:
        return True


def validateSalesCeditTermFormat(data: xml.etree.ElementTree.Element):
        try:
            salesConditionNode = data.find('eInvoiceNameSpace:CondicionVenta', namespaces).text
            if(salesConditionNode == "02"):
                creditTermNode = data.find('eInvoiceNameSpace:PlazoCredito', namespaces).text
                if len(creditTermNode) > 10:
                    return "Valor '" + creditTermNode + "' de nodo 'Plazo Crédito' excede límite de caracteres (10). " \
                                                        "Cantidad obtenida: " + str(len(creditTermNode))
                else:
                    return True
            else:
                return True
        except:
            return "Nodo 'PlazoCredito' en sección de encabezado está vacio o presenta algún problema"



def validatePaymentMethod(data: xml.etree.ElementTree.Element):
    PaymentMethodNode = data.findall('eInvoiceNameSpace:MedioPago', namespaces)
    if len(PaymentMethodNode) == 0:
        return "No existe Nodo 'MedioPago' en encabezado, el cual es de caracter obligatorio"
    else:
        return True


def validatePaymentMethodFormat(data: xml.etree.ElementTree.Element):
    acceptedPaymentMethods = ["01", "02", "03", "04", "05", "99"]
    try:
        paymentMethodNode = data.find('eInvoiceNameSpace:MedioPago', namespaces).text
        if len(paymentMethodNode) > 2 or paymentMethodNode not in acceptedPaymentMethods:
            return " El valor (" + paymentMethodNode + ") del nodo 'MedioPago' en la sección del encabezado" \
                   " no es válido con respecto al catálogo de tipos: " + str(acceptedPaymentMethods)
        else:
            return True
    except:
        return "Nodo 'MedioPago' en sección de encabezado está vacio o presenta algún problema"
