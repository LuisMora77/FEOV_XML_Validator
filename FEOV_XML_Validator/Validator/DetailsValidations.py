import xml.etree.ElementTree
import Validator.AuxiliarFunctions
import re


def validateDetailsInfo(data: xml.etree.ElementTree.Element):
    totalLineas = data.findall(".//DetalleServicio/LineaDetalle/NumeroLinea")
    #for i in range(len(totalLineas)):
        #print("Yahoo! \n")


def validateLineNumber(data: xml.etree.ElementTree.Element, position):
    try:
        numLinea = data.findall(".//DetalleServicio/LineaDetalle/NumeroLinea")[position].text
        if int(numLinea) < 1:
            return "Valor de nodo 'NumeroLinea' en sección DetalleServicio/LineaDetalle  no puede ser negativo. " \
                   "(LineaDetalle " + str(position) + ")"
        else:
            return True
    except:
        return "Valor de nodo 'NumeroLinea' no puede ser vacío."


def validateLineCabysCode(data: xml.etree.ElementTree.Element, position):
    try:
        cabysCode = data.findall(".//DetalleServicio/LineaDetalle/Codigo")[position].text
        if len(cabysCode) != 13:
            return "Valor de nodo 'Codigo' en seccion de DetalleServicio, línea " + position + " no posee un formato" \
                                                                                               "válido (13 caracteres)"
        else:
            return True
    except:
        return "Valor de nodo 'Codigo' en seccion 'DetalleServicio/LineaDetalle', no puede ser vacío."


def validateCommercialCodeType(data: xml.etree.ElementTree.Element, position):
    acceptedTypes = ["01", "02", "03", "04", "99"]
    try:
        commercialCodeType = data.findall(".//DetalleServicio/LineaDetalle/CodigoComercial/Tipo")[position].text
        if len(commercialCodeType) != 2 or commercialCodeType not in acceptedTypes:
            return "Valor de nodo 'Tipo' en seccion de DetalleServicio, línea " + position + " no posee " \
                                                                                             "un formato valido (2 caracteres) o no es valido con respecto al catalogo de tipos: " \
                   + str(acceptedTypes)
        else:
            return True
    except:
        return "Valor de nodo 'Tipo' en seccion 'DetalleServicio/LineaDetalle/CodigoComercial', no puede ser vacío."


def validateCommercialCodeCode(data: xml.etree.ElementTree.Element, position):
    try:
        commercialCodeCode = data.findall(".//DetalleServicio/LineaDetalle/CodigoComercial/Codigo")[position].text
        if len(commercialCodeCode) > 20:
            return "Valor de nodo 'Codigo' en seccion 'DetalleServicio/LineaDetalle/CodigoComercial', línea " \
                   + position + " no posee un formato válido (20 caracteres)"
        else:
            return True
    except:
        return "Valor de nodo 'Codigo' en seccion 'DetalleServicio/LineaDetalle/CodigoComercial', no puede ser vacío."


def validateQty(data: xml.etree.ElementTree.Element, position):
    try:
        QtyNode = data.findall(".//DetalleServicio/LineaDetalle/Cantidad")[position].text
        isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(QtyNode, 13, 3)
        if not isValidDecimal:
            return "Valor de nodo 'Cantidad' en seccion 'DetalleServicio/LineaDetalle', línea " \
                   + position + " no posee un formato válido (13 enteros (maximo), 3 decimales)"
        else:
            return True
    except:
        return "Valor de nodo 'Cantidad' en seccion 'DetalleServicio/LineaDetalle', no puede ser vacío."


def validateUnitOfMeasure(data: xml.etree.ElementTree.Element, position):
    try:
        UMNode = data.findall(".//DetalleServicio/LineaDetalle/UnidadMedida")[position].text
        if len(UMNode) > 15:
            return "Valor de nodo 'UnidadMedida' en seccion 'DetalleServicio/LineaDetalle', línea " \
                   + position + " no posee un formato válido (maximo 15 caracteres)"
        else:
            return True
    except:
        return "Valor de nodo 'UnidadMedida' en seccion 'DetalleServicio/LineaDetalle', no puede ser vacío."


def validateComercialUnitOfMeasure(data: xml.etree.ElementTree.Element, position):
    try:
        comercialUMNode = data.findall(".//DetalleServicio/LineaDetalle/UnidadMedidaComercial")[position].text
        if len(comercialUMNode) > 20:
            return "Valor de nodo 'UnidadMedidaComercial' en seccion 'DetalleServicio/LineaDetalle', línea " \
                   + position + " no posee un formato válido (maximo 20 caracteres)"
        else:
            return True
    except:
        return True


def validateDetail(data: xml.etree.ElementTree.Element, position):
    try:
        detailNode = data.findall(".//DetalleServicio/LineaDetalle/Detalle")[position].text
        if len(detailNode) > 200:
            return "Valor de nodo 'Detalle' en seccion 'DetalleServicio/LineaDetalle', línea " \
                   + position + " no posee un formato válido (maximo 200 caracteres)"
        else:
            return True
    except:
        return "Valor de nodo 'Detalle' en seccion 'DetalleServicio/LineaDetalle', no puede ser vacío."


def validateUnitPrice(data: xml.etree.ElementTree.Element, position):
    try:
        unitPriceNode = data.findall(".//DetalleServicio/LineaDetalle/PrecioUnitario")[position].text
        isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(unitPriceNode, 18, 5)
        if not isValidDecimal:
            return "Valor de nodo 'PrecioUnitario' en seccion 'DetalleServicio/LineaDetalle', línea " \
                   + position + " no posee un formato válido ( 18 enteros (maximo), 5 decimales)"
        else:
            return True
    except:
        return "Valor de nodo 'PrecioUnitario' en seccion 'DetalleServicio/LineaDetalle', no puede ser vacío."


def validateTotalAmount(data: xml.etree.ElementTree.Element, position):
    try:
        totalAmountNode = data.findall(".//DetalleServicio/LineaDetalle/PrecioUnitario")[position].text
        isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(totalAmountNode, 18, 5)
        if not isValidDecimal:
            return "Valor de nodo 'MontoTotal' en seccion 'DetalleServicio/LineaDetalle', línea " \
                   + position + " no posee un formato válido ( 18 enteros (maximo), 5 decimales)"
        else:
            return True
    except:
        return "Valor de nodo 'MontoTotal' en seccion 'DetalleServicio/LineaDetalle', no puede ser vacío."


def validateDiscount(data: xml.etree.ElementTree.Element, position):
    try:
        discountNode = data.findall(".//DetalleServicio/LineaDetalle/Descuento")[position].text
    except:
        return True
    try:
        discountAmountNode = data.findall(".//DetalleServicio/LineaDetalle/Descuento/MontoDescuento")[position].text
        isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(discountAmountNode, 18, 5)
        if not isValidDecimal:
            return "Valor de nodo 'MontoDescuento' en seccion 'DetalleServicio/LineaDetalle/Descuento', línea " \
                   + position + " no posee un formato válido (18 enteros (maximo), 5 decimales)"
        else:
            return True
    except:
        return "Valor de nodo 'MontoDescuento' en seccion 'DetalleServicio/LineaDetalle/Descuento', no puede ser vacío."


def validateDiscountReason(data: xml.etree.ElementTree.Element, position):
    try:
        discountNode = data.findall(".//DetalleServicio/LineaDetalle/Descuento")[position].text
    except:
        return True
    try:
        discountReasonNode = data.findall(".//DetalleServicio/LineaDetalle/Descuento/NaturalezaDescuento")[position].text
        isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(discountReasonNode, 18, 5)
        if not isValidDecimal:
            return "Valor de nodo 'NaturalezaDescuento' en seccion 'DetalleServicio/LineaDetalle/Descuento', línea " \
                   + position + " no posee un formato válido (maximo 80 caracteres)"
        else:
            return True
    except:
        return "Valor de nodo 'NaturalezaDescuento' en seccion 'DetalleServicio/LineaDetalle/Descuento', " \
                "no puede ser vacío."


def validateSubTotal(data: xml.etree.ElementTree.Element, position):
    try:
        subTotalNode = data.findall(".//DetalleServicio/LineaDetalle/SubTotal")[position].text
        isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(subTotalNode, 18, 5)
        if not isValidDecimal:
            return "Valor de nodo 'SubTotal' en seccion 'DetalleServicio/LineaDetalle', línea " \
                   + position + " no posee un formato válido (18 enteros (maximo), 5 decimales)"
        else:
            return True
    except:
        return "Valor de nodo 'SubTotal' en seccion 'DetalleServicio/LineaDetalle', no puede ser vacío."


def validateTaxBase(data: xml.etree.ElementTree.Element, position):
    try:
        taxCode = data.findall(".//DetalleServicio/LineaDetalle/Impuesto/Codigo")[position].text
        if taxCode == "07":
            try:
                taxBaseNode = data.findall(".//DetalleServicio/LineaDetalle/BaseImponible")[position].text
                isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(taxBaseNode, 18, 5)
                if not isValidDecimal:
                    return "Valor de nodo 'BaseImponible' en seccion 'DetalleServicio/LineaDetalle', línea " \
                        + position + " no posee un formato válido (18 enteros (maximo), 5 decimales)"
                else:
                    return True
            except:
                return "Valor de nodo 'BaseImponible' en seccion 'DetalleServicio/LineaDetalle', no puede ser vacío."
        else:
            return True
    except:
        return True


#def validateTaxCode(data: xml.etree.ElementTree.Element, position):
    #taxCode = data.findall(".//DetalleServicio/LineaDetalle/Impuesto/Codigo")[position].text
