import XMLValidator.Validator.AuxiliarFunctions as AuxiliarFunctions
import xml.etree.ElementTree
import re

# Namespace necesario al momento de obtener un nodo, sin esto no se pueden leer los datos del nodo.
namespaces = {'eInvoiceNameSpace': 'https://cdn.comprobanteselectronicos.go.cr/xml-schemas/v4.3/facturaElectronica'}
alphabetRegex = "^[a-zA-Z]+$"
totalNodesNames = ["TotalServGravados", "TotalServExentos", "TotalServExonerado", "TotalMercanciasGravadas",
                   "TotalMercanciasExentas", "TotalMercExonerada", "TotalGravado", "TotalExento", "TotalExonerado",
                   "TotalVenta", "TotalDescuentos", "TotalVentaNeta", "TotalImpuesto", "TotalIVADevuelto",
                   "TotalOtrosCargos", "TotalComprobante"]


def validateTotalsInfo(data: xml.etree.ElementTree.Element):
    einviceSummaryNode = data.find('eInvoiceNameSpace:ResumenFactura', namespaces)
    results = validateTotals(einviceSummaryNode, totalNodesNames, data)
    results.append(validateCurrencyCode(einviceSummaryNode))
    results.append(validateExchangeRate(einviceSummaryNode))
    formattedTotalsResults = AuxiliarFunctions.flattenList(results)
    return formattedTotalsResults


def checkOtherChargesNode(data: xml.etree.ElementTree.Element, nodesList):
    otherChargesNode = data.find('eInvoiceNameSpace:OtrosCargos', namespaces)
    print("otherChargesNode", otherChargesNode)
    if otherChargesNode == None:
        nodesList.remove("TotalOtrosCargos")
    return nodesList


def validateTotals(einviceSummaryNode, nodesList, data):
    results = []
    finalNodeList = checkOtherChargesNode(data, nodesList)
    for nodeName in finalNodeList:
        try:
            totalNode = einviceSummaryNode.find('eInvoiceNameSpace:' + nodeName, namespaces).text
            isValidDecimal = AuxiliarFunctions.validateDecimal(totalNode, 18, 5)
            if not isValidDecimal:
                results.append(" Valor de nodo '" + nodeName + "' en sección './/ResumenFactura , no posee un formato"
                               " válido (18 enteros (máximo), 5 decimales. Recibido: " + totalNode + ")")
            else:
                results.append(True)
        except:
            results.append("Valor de nodo '" + nodeName + "' en sección './/ResumenFactura, no puede ser vacío.")
    return results

def validateCurrencyCode(data: xml.etree.ElementTree.Element):
    try:
        currencyCodeTypeNode = data.find('eInvoiceNameSpace:CodigoTipoMoneda', namespaces)
        currencyCodeNode = currencyCodeTypeNode.find('eInvoiceNameSpace:CodigoMoneda', namespaces).text
        checkOnlyLetters = re.match(alphabetRegex, currencyCodeNode)
        if len(currencyCodeNode) != 3 or checkOnlyLetters == None:
            return " Valor de nodo 'CodigoMondeda' en sección './/ResumenFactura/CodigoTipoMoneda, no posee un" \
                   " formato válido (3 letras)."
        else:
            return True
    except:
        return "Valor de nodo 'CodigoMondeda' en sección './/ResumenFactura/CodigoTipoMoneda, no puede ser vacío."


def validateExchangeRate(data: xml.etree.ElementTree.Element):
    try:
        currencyCodeTypeNode = data.find('eInvoiceNameSpace:CodigoTipoMoneda', namespaces)
        ExchangeRateNode = currencyCodeTypeNode.find('eInvoiceNameSpace:TipoCambio', namespaces).text
        isValidDecimal = AuxiliarFunctions.validateDecimal(ExchangeRateNode, 18, 5)
        if not isValidDecimal:
            return "Valor de nodo 'TipoCambio' en sección './/ResumenFactura/CodigoTipoMoneda, no posee un " \
                   "formato válido (18 enteros (máximo), 5 decimales. Recibido: " + ExchangeRateNode + ")"
        else:
            return True
    except:
        return "Valor de nodo 'TipoCambio' en sección './/ResumenFactura/CodigoTipoMoneda, no puede ser vacío."
