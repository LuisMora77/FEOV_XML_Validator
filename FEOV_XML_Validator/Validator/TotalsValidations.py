import Validator.AuxiliarFunctions
import xml.etree.ElementTree
import re

alphabetRegex = "^[a-zA-Z]+$"
totalNodesNames = ["TotalServGravados", "TotalServExentos", "TotalServExonerado", "TotalMercanciasGravadas",
                   "TotalMercanciasExentas", "TotalMercExonerada", "TotalGravado", "TotalExento", "TotalExonerado",
                   "TotalVenta", "TotalDescuentos", "TotalVentaNeta", "TotalImpuesto", "TotalIVADevuelto",
                   "TotalOtrosCargos", "TotalComprobante"]


def validateTotalsInfo(data: xml.etree.ElementTree.Element):
    results = validateTotals(data, totalNodesNames)
    results.append(validateCurrencyCode(data))
    results.append(validateExchangeRate(data))
    formattedTotalsResults = Validator.AuxiliarFunctions.flattenList(results)
    return formattedTotalsResults


def validateTotals(data: xml.etree.ElementTree.Element, nodesList):
    results = []
    for nodeName in nodesList:
        try:
            totalNode = data.findall(".//ResumenFactura/" + nodeName)[0].text
            isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(totalNode, 18, 5)
            if not isValidDecimal:
                return "Valor de nodo '" + nodeName + "' en sección './/ResumenFactura , no posee un " \
                       "formato válido (18 enteros (máximo), 5 decimales. Recibido: " + totalNode + ")"
            else:
                results.append(True)
        except:
            results.append("Valor de nodo '" + nodeName + "' en sección './/ResumenFactura, no puede ser vacío.")
    return results

def validateCurrencyCode(data: xml.etree.ElementTree.Element):
    try:
        currencyCodeNode = data.findall(".//ResumenFactura/CodigoTipoMoneda/CodigoMondeda")[0].text
        checkOnlyLetters = re.match(alphabetRegex, currencyCodeNode)
        if len(currencyCodeNode) != 3 or checkOnlyLetters == None:
            return "Valor de nodo 'CodigoMondeda' en sección './/ResumenFactura/CodigoTipoMoneda, no posee un " \
                                  "formato válido (3 letras)."
        else:
            return True
    except:
        return "Valor de nodo 'CodigoMondeda' en sección './/ResumenFactura/CodigoTipoMoneda, no puede ser vacío."


def validateExchangeRate(data: xml.etree.ElementTree.Element):
    try:
        ExchangeRateNode = data.findall(".//ResumenFactura/CodigoTipoMoneda/TipoCambio")[0].text
        isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(ExchangeRateNode, 18, 5)
        if not isValidDecimal:
            return "Valor de nodo 'TipoCambio' en sección './/ResumenFactura/CodigoTipoMoneda, no posee un " \
                   "formato válido (18 enteros (máximo), 5 decimales. Recibido: " + ExchangeRateNode + ")"
        else:
            return True
    except:
        return "Valor de nodo 'TipoCambio' en sección './/ResumenFactura/CodigoTipoMoneda, no puede ser vacío."


# def validateTaxedServicesTotal(data: xml.etree.ElementTree.Element):
#     try:
#         totalNode = data.findall(".//ResumenFactura/TotalServGravados")[0].text
#         isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(totalNode, 18, 5)
#         if not isValidDecimal:
#             return "Valor de nodo 'TotalServGravados' en sección './/ResumenFactura , no posee un " \
#                    "formato válido (18 enteros (máximo), 5 decimales. Recibido: " + totalNode + ")"
#         else:
#             return True
#     except:
#         return "Valor de nodo 'TotalServGravados' en sección './/ResumenFactura, no puede ser vacío."
#
#
# def validateExentServicesTotal(data: xml.etree.ElementTree.Element):
#     try:
#         totalNode = data.findall(".//ResumenFactura/TotalServExentos")[0].text
#         isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(totalNode, 18, 5)
#         if not isValidDecimal:
#             return "Valor de nodo 'TotalServExentos' en sección './/ResumenFactura , no posee un " \
#                    "formato válido (18 enteros (máximo), 5 decimales. Recibido: " + totalNode + ")"
#         else:
#             return True
#     except:
#         return "Valor de nodo 'TotalServExentos' en sección './/ResumenFactura, no puede ser vacío."
#
#
# def validateExoneratedServicesTotal(data: xml.etree.ElementTree.Element):
#     try:
#         totalNode = data.findall(".//ResumenFactura/TotalServExonerado")[0].text
#         isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(totalNode, 18, 5)
#         if not isValidDecimal:
#             return "Valor de nodo 'TotalServExonerado' en sección './/ResumenFactura , no posee un " \
#                    "formato válido (18 enteros (máximo), 5 decimales. Recibido: " + totalNode + ")"
#         else:
#             return True
#     except:
#         return "Valor de nodo 'TotalServExonerado' en sección './/ResumenFactura, no puede ser vacío."
#
#
# def validateTaxedArticlesTotal(data: xml.etree.ElementTree.Element):
#     try:
#         totalNode = data.findall(".//ResumenFactura/TotalMercanciasGravadas")[0].text
#         isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(totalNode, 18, 5)
#         if not isValidDecimal:
#             return "Valor de nodo 'TotalMercanciasGravadas' en sección './/ResumenFactura , no posee un " \
#                    "formato válido (18 enteros (máximo), 5 decimales. Recibido: " + totalNode + ")"
#         else:
#             return True
#     except:
#         return "Valor de nodo 'TotalMercanciasGravadas' en sección './/ResumenFactura, no puede ser vacío."
#
#
# def validateExentArticlesTotal(data: xml.etree.ElementTree.Element):
#     try:
#         totalNode = data.findall(".//ResumenFactura/TotalMercanciasExentas")[0].text
#         isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(totalNode, 18, 5)
#         if not isValidDecimal:
#             return "Valor de nodo 'TotalMercanciasExentas' en sección './/ResumenFactura , no posee un " \
#                    "formato válido (18 enteros (máximo), 5 decimales. Recibido: " + totalNode + ")"
#         else:
#             return True
#     except:
#         return "Valor de nodo 'TotalMercanciasExentas' en sección './/ResumenFactura, no puede ser vacío."
#
#
# def validateExoneratedArticlesTotal(data: xml.etree.ElementTree.Element):
#     try:
#         totalNode = data.findall(".//ResumenFactura/TotalMercExonerada")[0].text
#         isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(totalNode, 18, 5)
#         if not isValidDecimal:
#             return "Valor de nodo 'TotalMercExonerada' en sección './/ResumenFactura , no posee un " \
#                    "formato válido (18 enteros (máximo), 5 decimales. Recibido: " + totalNode + ")"
#         else:
#             return True
#     except:
#         return "Valor de nodo 'TotalMercExonerada' en sección './/ResumenFactura, no puede ser vacío."
#
#
# def validateTaxedTotal(data: xml.etree.ElementTree.Element):
#     try:
#         totalNode = data.findall(".//ResumenFactura/TotalGravado")[0].text
#         isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(totalNode, 18, 5)
#         if not isValidDecimal:
#             return "Valor de nodo 'TotalGravado' en sección './/ResumenFactura , no posee un " \
#                    "formato válido (18 enteros (máximo), 5 decimales. Recibido: " + totalNode + ")"
#         else:
#             return True
#     except:
#         return "Valor de nodo 'TotalGravado' en sección './/ResumenFactura, no puede ser vacío."
#
#
# def validateExentTotal(data: xml.etree.ElementTree.Element):
#     try:
#         totalNode = data.findall(".//ResumenFactura/TotalExento")[0].text
#         isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(totalNode, 18, 5)
#         if not isValidDecimal:
#             return "Valor de nodo 'TotalExento' en sección './/ResumenFactura , no posee un " \
#                    "formato válido (18 enteros (máximo), 5 decimales. Recibido: " + totalNode + ")"
#         else:
#             return True
#     except:
#         return "Valor de nodo 'TotalExento' en sección './/ResumenFactura, no puede ser vacío."
#
#
# def validateExoneratedTotal(data: xml.etree.ElementTree.Element):
#     try:
#         totalNode = data.findall(".//ResumenFactura/TotalExonerado")[0].text
#         isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(totalNode, 18, 5)
#         if not isValidDecimal:
#             return "Valor de nodo 'TotalExonerado' en sección './/ResumenFactura , no posee un " \
#                    "formato válido (18 enteros (máximo), 5 decimales. Recibido: " + totalNode + ")"
#         else:
#             return True
#     except:
#         return "Valor de nodo 'TotalExonerado' en sección './/ResumenFactura, no puede ser vacío."
#
#
# def validateSalesTotal(data: xml.etree.ElementTree.Element):
#     try:
#         totalNode = data.findall(".//ResumenFactura/TotalVenta")[0].text
#         isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(totalNode, 18, 5)
#         if not isValidDecimal:
#             return "Valor de nodo 'TotalVenta' en sección './/ResumenFactura , no posee un " \
#                    "formato válido (18 enteros (máximo), 5 decimales. Recibido: " + totalNode + ")"
#         else:
#             return True
#     except:
#         return "Valor de nodo 'TotalVenta' en sección './/ResumenFactura, no puede ser vacío."
#
#
# def validateDiscountsTotal(data: xml.etree.ElementTree.Element):
#     try:
#         totalNode = data.findall(".//ResumenFactura/TotalDescuentos")[0].text
#         isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(totalNode, 18, 5)
#         if not isValidDecimal:
#             return "Valor de nodo 'TotalDescuentos' en sección './/ResumenFactura , no posee un " \
#                    "formato válido (18 enteros (máximo), 5 decimales. Recibido: " + totalNode + ")"
#         else:
#             return True
#     except:
#         return "Valor de nodo 'TotalDescuentos' en sección './/ResumenFactura, no puede ser vacío."
#
#
# def validateNetSalesTotal(data: xml.etree.ElementTree.Element):
#     try:
#         totalNode = data.findall(".//ResumenFactura/TotalVentaNeta")[0].text
#         isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(totalNode, 18, 5)
#         if not isValidDecimal:
#             return "Valor de nodo 'TotalVentaNeta' en sección './/ResumenFactura , no posee un " \
#                    "formato válido (18 enteros (máximo), 5 decimales. Recibido: " + totalNode + ")"
#         else:
#             return True
#     except:
#         return "Valor de nodo 'TotalVentaNeta' en sección './/ResumenFactura, no puede ser vacío."
