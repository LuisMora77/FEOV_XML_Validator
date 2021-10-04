import xml.etree.ElementTree
import Validator.AuxiliarFunctions
import re


def validateDetailsInfo(data: xml.etree.ElementTree.Element):
    totalLineas = data.findall(".//DetalleServicio/LineaDetalle/NumeroLinea")
    results = []
    for i in range(len(totalLineas)):
        results.append(validateLineNumber(data, i))
        results.append(validateLineCabysCode(data, i))
        results.append(validateCommercialCodeType(data, i))
        results.append(validateCommercialCodeCode(data, i))
        results.append(validateQty(data, i))
        results.append(validateUnitOfMeasure(data, i))
        results.append(validateComercialUnitOfMeasure(data, i))
        results.append(validateDetail(data, i))
        results.append(validateUnitPrice(data, i))
        results.append(validateTotalAmount(data, i))
        results.append(validateDiscount(data, i))
        results.append(validateDiscountReason(data, i))
        results.append(validateSubTotal(data, i))
        results.append(validateTaxBase(data, i))
        results.append(validateTaxCode(data, i))
        results.append(validateTaxRateCode(data, i))
        results.append(validateTaxRate(data, i))
        results.append(validateAmount(data, i))
        results.append(validateExonerationDocumentType(data, i))
        results.append(validateDocNumber(data, i))
        results.append(validateInstitutionName(data, i))
        results.append(validateSentDate(data, i))
        results.append(validateExemptionPercentage(data, i))
        results.append(validateExemptionAmount(data, i))
        results.append(validateNetTax(data, i))
        results.append(validateTotalLineAmount(data, i))
        results.append(validateOtherChargesDocuemntType(data, i))
        results.append(validateThirdPartysName(data, i))
        results.append(validateOCDetail(data, i))
        results.append(validateOCPercent(data, i))
        results.append(validateChargeAmount(data, i))

    formattedDetailResults = Validator.AuxiliarFunctions.flattenList(results)
    return formattedDetailResults


def validateLineNumber(data: xml.etree.ElementTree.Element, position):
    try:
        numLinea = data.findall(".//DetalleServicio/LineaDetalle/NumeroLinea")[position].text
        if int(numLinea) < 1:
            return "Valor de nodo 'NumeroLinea' en sección DetalleServicio/LineaDetalle  no puede ser negativo. " \
                   "(LineaDetalle " + str(position + 1) + ")"
        else:
            return True
    except:
        return "Valor de nodo 'NumeroLinea' no puede ser vacío."


def validateLineCabysCode(data: xml.etree.ElementTree.Element, position):
    try:
        cabysCode = data.findall(".//DetalleServicio/LineaDetalle/Codigo")[position].text
        if len(cabysCode) != 13:
            return "Valor de nodo 'Codigo' en sección de DetalleServicio, línea " + str(
                position + 1) + ", no posee un formato válido (13 caracteres. Recibido: " + cabysCode + ")"
        else:
            return True
    except:
        return "Valor de nodo 'Codigo' en sección 'DetalleServicio/LineaDetalle', no puede ser vacío."


def validateCommercialCodeType(data: xml.etree.ElementTree.Element, position):
    acceptedTypes = ["01", "02", "03", "04", "99"]
    try:
        commercialCodeType = data.findall(".//DetalleServicio/LineaDetalle/CodigoComercial/Tipo")[position].text
        if len(commercialCodeType) != 2 or commercialCodeType not in acceptedTypes:
            return "Valor (" + commercialCodeType + ") de nodo 'Tipo' en sección de DetalleServicio, línea " \
                   + str(position + 1) + ",no es válido con respecto al catalogo de tipos: " + str(acceptedTypes)
        else:
            return True
    except:
        return "Valor de nodo 'Tipo' en sección 'DetalleServicio/LineaDetalle/CodigoComercial', no puede ser vacío."


def validateCommercialCodeCode(data: xml.etree.ElementTree.Element, position):
    try:
        commercialCodeCode = data.findall(".//DetalleServicio/LineaDetalle/CodigoComercial/Codigo")[position].text
        if len(commercialCodeCode) > 20:
            return "Valor de nodo 'Codigo' en sección 'DetalleServicio/LineaDetalle/CodigoComercial', línea " \
                   + str(position + 1) + " no posee un formato válido (20 caracteres)"
        else:
            return True
    except:
        return "Valor de nodo 'Codigo' en sección 'DetalleServicio/LineaDetalle/CodigoComercial', no puede ser vacío."


def validateQty(data: xml.etree.ElementTree.Element, position):
    try:
        QtyNode = data.findall(".//DetalleServicio/LineaDetalle/Cantidad")[position].text
        isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(QtyNode, 13, 3)
        if not isValidDecimal:
            return "Valor de nodo 'Cantidad' en sección 'DetalleServicio/LineaDetalle', línea " \
                   + str(position + 1) + " no posee un formato válido (13 enteros (máximo), 3 decimales)"
        else:
            return True
    except:
        return "Valor de nodo 'Cantidad' en sección 'DetalleServicio/LineaDetalle', no puede ser vacío."


def validateUnitOfMeasure(data: xml.etree.ElementTree.Element, position):
    try:
        UMNode = data.findall(".//DetalleServicio/LineaDetalle/UnidadMedida")[position].text
        if len(UMNode) > 15:
            return "Valor de nodo 'UnidadMedida' en sección 'DetalleServicio/LineaDetalle', línea " \
                   + str(position + 1) + " no posee un formato válido (máximo 15 caracteres)"
        else:
            return True
    except:
        return "Valor de nodo 'UnidadMedida' en sección 'DetalleServicio/LineaDetalle', no puede ser vacío."


def validateComercialUnitOfMeasure(data: xml.etree.ElementTree.Element, position):
    try:
        comercialUMNode = data.findall(".//DetalleServicio/LineaDetalle/UnidadMedidaComercial")[position].text
        if len(comercialUMNode) > 20:
            return "Valor de nodo 'UnidadMedidaComercial' en sección 'DetalleServicio/LineaDetalle', línea " \
                   + str(position + 1) + " no posee un formato válido (máximo 20 caracteres)"
        else:
            return True
    except:
        return True


def validateDetail(data: xml.etree.ElementTree.Element, position):
    try:
        detailNode = data.findall(".//DetalleServicio/LineaDetalle/Detalle")[position].text
        if len(detailNode) > 200:
            return "Valor de nodo 'Detalle' en sección 'DetalleServicio/LineaDetalle', línea " \
                   + str(position + 1) + " no posee un formato válido (máximo 200 caracteres. Recibido:" \
                   + str(len(detailNode)) + " caracteres)"
        else:
            return True
    except:
        return "Valor de nodo 'Detalle' en sección 'DetalleServicio/LineaDetalle', no puede ser vacío."


def validateUnitPrice(data: xml.etree.ElementTree.Element, position):
    try:
        unitPriceNode = data.findall(".//DetalleServicio/LineaDetalle/PrecioUnitario")[position].text
        isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(unitPriceNode, 18, 5)
        if not isValidDecimal:
            return "Valor de nodo 'PrecioUnitario' en sección 'DetalleServicio/LineaDetalle', línea " \
                   + str(position + 1) + " no posee un formato válido ( 18 enteros (máximo), 5 decimales. Recibido: " \
                   + unitPriceNode + ")"
        else:
            return True
    except:
        return "Valor de nodo 'PrecioUnitario' en sección 'DetalleServicio/LineaDetalle', no puede ser vacío."


def validateTotalAmount(data: xml.etree.ElementTree.Element, position):
    try:
        totalAmountNode = data.findall(".//DetalleServicio/LineaDetalle/MontoTotal")[position].text
        isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(totalAmountNode, 18, 5)
        if not isValidDecimal:
            return "Valor de nodo 'MontoTotal' en sección 'DetalleServicio/LineaDetalle', línea " \
                   + str(position + 1) + " no posee un formato válido ( 18 enteros (máximo), 5 decimales. Recibido: " \
                   + totalAmountNode + ")"
        else:
            return True
    except:
        return "Valor de nodo 'MontoTotal' en sección 'DetalleServicio/LineaDetalle', no puede ser vacío."


def validateDiscount(data: xml.etree.ElementTree.Element, position):
    try:
        discountNode = data.findall(".//DetalleServicio/LineaDetalle/Descuento")[position].text
    except:
        return True
    try:
        discountAmountNode = data.findall(".//DetalleServicio/LineaDetalle/Descuento/MontoDescuento")[position].text
        isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(discountAmountNode, 18, 5)
        if not isValidDecimal:
            return "Valor de nodo 'MontoDescuento' en sección 'DetalleServicio/LineaDetalle/Descuento', línea " \
                   + str(position + 1) + " no posee un formato válido (18 enteros (máximo), 5 decimales. Recibido: " \
                   + discountAmountNode + ")"
        else:
            return True
    except:
        return "Valor de nodo 'MontoDescuento' en sección 'DetalleServicio/LineaDetalle/Descuento', no puede ser vacío."


def validateDiscountReason(data: xml.etree.ElementTree.Element, position):
    discountNode = data.findall(".//DetalleServicio/LineaDetalle/Descuento")
    if len(discountNode) > 0:
        try:
            discountReasonNode = data.findall(".//DetalleServicio/LineaDetalle/Descuento/NaturalezaDescuento")[
                position].text
            if len(discountReasonNode) > 80:
                return "Valor de nodo 'NaturalezaDescuento' en sección 'DetalleServicio/LineaDetalle/Descuento', línea " \
                       + str(position + 1) + " no posee un formato válido (máximo 80 caracteres)"
            else:
                return True
        except:
            return "Valor de nodo 'NaturalezaDescuento' en sección 'DetalleServicio/LineaDetalle/Descuento', " \
                   "no puede ser vacío."
    else:
        return True


def validateSubTotal(data: xml.etree.ElementTree.Element, position):
    try:
        subTotalNode = data.findall(".//DetalleServicio/LineaDetalle/SubTotal")[position].text
        isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(subTotalNode, 18, 5)
        if not isValidDecimal:
            return "Valor de nodo 'SubTotal' en sección 'DetalleServicio/LineaDetalle', línea " \
                   + str(position + 1) + " no posee un formato válido (18 enteros (máximo), 5 decimales. Recibido: " \
                   + subTotalNode + ")"
        else:
            return True
    except:
        return "Valor de nodo 'SubTotal' en sección 'DetalleServicio/LineaDetalle', no puede ser vacío."


def validateTaxBase(data: xml.etree.ElementTree.Element, position):
    try:
        taxCode = data.findall(".//DetalleServicio/LineaDetalle/Impuesto/Codigo")[position].text
        if taxCode == "07":
            try:
                taxBaseNode = data.findall(".//DetalleServicio/LineaDetalle/BaseImponible")[position].text
                isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(taxBaseNode, 18, 5)
                if not isValidDecimal:
                    return "Valor de nodo 'BaseImponible' en sección 'DetalleServicio/LineaDetalle', línea " \
                           + str(position + 1) + " no posee un formato válido (18 enteros (máximo), 5 decimales. Recibido: " \
                   + taxBaseNode + ")"
                else:
                    return True
            except:
                return "Valor de nodo 'BaseImponible' en sección 'DetalleServicio/LineaDetalle', no puede ser vacío."
        else:
            return True
    except:
        return True


def validateTaxCode(data: xml.etree.ElementTree.Element, position):
    acceptedCodes = ["01", "02", "03", "04", "05", "06", "07", "08", "12", "99"]
    # acceptedCodes = ["01", "02", "03", "04", "05", "06", "07", "08"]
    try:
        taxCode = data.findall(".//DetalleServicio/LineaDetalle/Impuesto/Codigo")[position].text
        if len(taxCode) != 2 or taxCode not in acceptedCodes:
            return "Valor (" + taxCode +") de nodo 'Codigo' en sección DetalleServicio/LineaDetalle/Impuesto, línea " + str(
                position + 1) + " no es válido con respecto al catalogo de tipos: " + str(acceptedCodes)
        else:
            return True
    except:
        return "Valor de nodo 'Codigo' en sección 'DetalleServicio/LineaDetalle/Impuesto', no puede ser vacío."


def validateTaxRateCode(data: xml.etree.ElementTree.Element, position):
    acceptedCodes = ["01", "02", "03", "04", "05", "06", "07", "08"]
    try:
        taxRateCodNode = data.findall(".//DetalleServicio/LineaDetalle/Impuesto/CodigoTarifa")[position].text
        if len(taxRateCodNode) != 2 or taxRateCodNode not in acceptedCodes:
            return "Valor de nodo 'CodigoTarifa' en sección DetalleServicio/LineaDetalle/Impuesto, línea " \
                   + str(
                position + 1) + " no posee un formato válido (2 caracteres) o no es válido con respecto al catalogo" \
                                " de tipos: " + str(acceptedCodes)
        else:
            return True
    except:
        return "Valor de nodo 'CodigoTarifa' en sección 'DetalleServicio/LineaDetalle/Impuesto', no puede ser vacío."


def validateTaxRate(data: xml.etree.ElementTree.Element, position):
    try:
        taxRateNode = data.findall(".//DetalleServicio/LineaDetalle/Impuesto/Tarifa")[position].text
        isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(taxRateNode, 4, 5)
        if not isValidDecimal:
            return "Valor de nodo 'Tarifa' en sección 'DetalleServicio/LineaDetalle/Impuesto', línea " \
                   + str(position + 1) + " no posee un formato válido (18 enteros (máximo), 5 decimales. Recibido: " \
                   + taxRateNode + ")"
        else:
            return True
    except:
        return "Valor de nodo 'Tarifa' en sección 'DetalleServicio/LineaDetalle/Impuesto', no puede ser vacío."


def validateAmount(data: xml.etree.ElementTree.Element, position):
    try:
        amountNode = data.findall(".//DetalleServicio/LineaDetalle/Impuesto/Monto")[position].text
        isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(amountNode, 18, 5)
        if not isValidDecimal:
            return "Valor de nodo 'Monto' en sección 'DetalleServicio/LineaDetalle/Impuesto', línea " \
                   + str(position + 1) + " no posee un formato válido (18 enteros (máximo), 5 decimales)"
        else:
            return True
    except:
        return "Valor de nodo 'Monto' en sección 'DetalleServicio/LineaDetalle/Impuesto/Monto', no puede ser vacío."


def validateExonerationDocumentType(data: xml.etree.ElementTree.Element, position):
    try:
        amountNode = data.findall(".//DetalleServicio/LineaDetalle/Impuesto/Exoneracion")[position]
        if amountNode:
            acceptedTypes = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "99"]
            try:
                docTypeNode = data.findall(".//DetalleServicio/LineaDetalle/Impuesto/Exoneracion/TipoDocumento")[
                    position].text
                if len(docTypeNode) != 2 or docTypeNode not in acceptedTypes:
                    return "Valor de nodo 'TipoDocumento' en sección DetalleServicio/LineaDetalle/Impuesto/Exoneracion, línea " \
                           + str(
                        position + 1) + " no posee un formato válido (2 caracteres) o no es válido con respecto al catalogo" \
                                        " de tipos: " + str(acceptedTypes)
                else:
                    return True
            except:
                return "Valor de nodo 'TipoDocumento' en sección 'DetalleServicio/LineaDetalle/Impuesto/Exoneracion', no " \
                       "puede ser vacío."
    except:
        return True


def validateDocNumber(data: xml.etree.ElementTree.Element, position):
    exonerationNode = data.findall(".//DetalleServicio/LineaDetalle/Impuesto/Exoneracion")
    if len(exonerationNode) > 0:
        try:
            docNum = data.findall(".//DetalleServicio/LineaDetalle/Impuesto/Exoneracion/NumeroDocumento")[position].text
            if len(docNum) > 40:
                return "Valor de nodo 'NumeroDocumento' en sección 'DetalleServicio/LineaDetalle/Impuesto', línea " \
                       + str(position + 1) + " no posee un formato válido (máximo 40 caracteres). "
            else:
                return True
        except:
            return "Valor de nodo 'NumeroDocumento' en sección 'DetalleServicio/LineaDetalle/Impuesto/Exoneracion', " \
                   "no puede ser vacío."
    else:
        return True


def validateInstitutionName(data: xml.etree.ElementTree.Element, position):
    exonerationNode = data.findall(".//DetalleServicio/LineaDetalle/Impuesto/Exoneracion")
    if len(exonerationNode) != 0:
        try:
            instName = data.findall(".//DetalleServicio/LineaDetalle/Impuesto/Exoneracion/NombreInstitucion")[
                position].text
            if len(instName) > 160:
                return "Valor de nodo 'NombreInstitucion' en sección 'DetalleServicio/LineaDetalle/Impuesto/ " \
                       "Exoneracion/NombreInstitucion', línea " \
                       + str(position + 1) + " no posee un formato válido (máximo 160 caracteres)."
            else:
                return True
        except:
            return "Valor de nodo 'NombreInstitucion' en sección 'DetalleServicio/LineaDetalle/Impuesto/Exoneracion" \
                   "/NombreInstitucion', no puede ser vacío."
    else:
        return True


def validateSentDate(data: xml.etree.ElementTree.Element, position):
    exonerationNode = data.findall(".//DetalleServicio/LineaDetalle/Impuesto/Exoneracion")
    if len(exonerationNode) != 0:
        try:
            dateNode = data.findall(".//DetalleServicio/LineaDetalle/Impuesto/Exoneracion/FechaEmision")[position].text
            if dateNode:
                return True
        except:
            return "Valor de nodo 'FechaEmision' en sección 'DetalleServicio/LineaDetalle/Impuesto/Exoneracion" \
                   "/FechaEmision', no puede ser vacío."
    else:
        return True


def validateExemptionPercentage(data: xml.etree.ElementTree.Element, position):
    exonerationNode = data.findall(".//DetalleServicio/LineaDetalle/Impuesto/Exoneracion")
    if len(exonerationNode) != 0:
        try:
            ExemptionNode = data.findall(".//DetalleServicio/LineaDetalle/Impuesto/Exoneracion/PorcentajeExoneracion")[
                position].text
            if len(ExemptionNode) > 3:
                return "Valor de nodo 'PorcentajeExoneracion' en sección 'DetalleServicio/LineaDetalle/Impuesto/ " \
                       "Exoneracion', línea " + str(position + 1) + " no posee un formato válido (máximo 3 caracteres)."
            else:
                return True
        except:
            return "Valor de nodo 'PorcentajeExoneracion' en sección 'DetalleServicio/LineaDetalle/Impuesto/" \
                   "Exoneracion, no puede ser vacío."
    else:
        return True


def validateExemptionAmount(data: xml.etree.ElementTree.Element, position):
    exonerationNode = data.findall(".//DetalleServicio/LineaDetalle/Impuesto/Exoneracion")
    if len(exonerationNode) != 0:
        try:
            ExemptionAmountNode = data.findall(".//DetalleServicio/LineaDetalle/Impuesto/Exoneracion/MontoExoneracion")[
                position].text
            isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(ExemptionAmountNode, 18, 5)
            if not isValidDecimal:
                return "Valor de nodo 'MontoExoneracion' en sección 'DetalleServicio/LineaDetalle/Impuesto/Exoneracion', línea " \
                       + str(position + 1) + " no posee un formato válido (18 enteros (máximo), 5 decimales. Recibido: " \
                   + ExemptionAmountNode + ")"
            else:
                return True
        except:
            return "Valor de nodo 'MontoExoneracion' en sección 'DetalleServicio/LineaDetalle/Impuesto/Exoneracion" \
                   "/FechaEmision', no puede ser vacío."
    else:
        return True


def validateNetTax(data: xml.etree.ElementTree.Element, position):
    netTaxNode = data.findall(".//DetalleServicio/LineaDetalle/ImpuestoNeto")
    if len(netTaxNode) > 0:
        try:
            netTaxStr = netTaxNode[position].text
            isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(netTaxStr, 18, 5)
            if not isValidDecimal:
                return "Valor de nodo 'ImpuestoNeto' en sección 'DetalleServicio/LineaDetalle', línea " \
                       + str(position + 1) + " no posee un formato válido (18 enteros (máximo), 5 decimales. Recibido: " \
                   + netTaxStr + ")"
            else:
                return True
        except:
            return "Valor de nodo 'ImpuestoNeto' en sección 'DetalleServicio/LineaDetalle, no puede ser vacío."
    else:
        return "No se encuenta nodo 'ImpuestoNeto' en lineaDetalle " + position + \
               ", el cual es de caracter obligatorio."


def validateTotalLineAmount(data: xml.etree.ElementTree.Element, position):
    TLANode = data.findall(".//DetalleServicio/LineaDetalle/MontoTotalLinea")
    if len(TLANode) > 0:
        try:
            TLAStr = TLANode[position].text
            isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(TLAStr, 18, 5)
            if not isValidDecimal:
                return "Valor de nodo 'MontoTotalLinea' en sección 'DetalleServicio/LineaDetalle', línea " \
                       + str(position + 1) + " no posee un formato válido (18 enteros (máximo), 5 decimales. Recibido: " \
                   + TLAStr + ")"
            else:
                return True
        except:
            return "Valor de nodo 'MontoTotalLinea' en sección 'DetalleServicio/LineaDetalle, no puede ser vacío."
    else:
        return "No se encuenta nodo 'MontoTotalLinea' en lineaDetalle " + position + \
               ", el cual es de caracter obligatorio."


def validateOtherChargesDocuemntType(data: xml.etree.ElementTree.Element, position):
    acceptedDocTypes = ["01", "02", "03", "04", "05", "06", "07", "99"]
    otherChargesNode = data.findall(".//OtrosCargos")
    if len(otherChargesNode) > 0:
        try:
            OCDocTypeNode = data.findall(".//OtrosCargos/TipoDocumento")[position].text
            if len(OCDocTypeNode) != 2 or OCDocTypeNode not in acceptedDocTypes:
                return "Valor de nodo 'TipoDocumento' en sección 'OtrosCargos', línea " + str(
                    position + 1) + " no posee un " \
                                    "formato válido (2 caracteres) o no es válido con respecto al catalogo de tipos: " \
                       + str(acceptedDocTypes)
            else:
                return True
        except:
            return "Valor de nodo 'TipoDocumento' en sección './/OtrosCargos, no puede ser vacío."
    else:
        return True


def validateThirdPartysName(data: xml.etree.ElementTree.Element, position):
    otherChargesNode = data.findall(".//OtrosCargos")
    if len(otherChargesNode) > 0:
        try:
            OCDocTypeNode = data.findall(".//OtrosCargos/TipoDocumento")[position].text
            if OCDocTypeNode == "04":
                try:
                    nameNode = data.findall(".//OtrosCargos/NombreTercero")[position].text
                    if len(nameNode) > 100:
                        return "Valor de nodo 'NombreTercero' en sección 'OtrosCargos', línea " \
                               + str(position + 1) + " no posee un formato válido (máximo 100 caracteres, caracteres" \
                                                     " recibidos: " + str(len(nameNode)) + ")"
                    else:
                        return True
                except:
                    return "Valor de nodo 'NombreTercero' en sección './/OtrosCargos, no puede ser vacío."
            else:
                return True
        except:
            return "Valor de nodo 'TipoDocumento' en sección './/OtrosCargos, no puede ser vacío."
    else:
        return True


def validateOCDetail(data: xml.etree.ElementTree.Element, position):
    otherChargesNode = data.findall(".//OtrosCargos")
    if len(otherChargesNode) > 0:
        try:
            detailsNode = data.findall(".//OtrosCargos/Detalle")[position].text
            if len(detailsNode) > 160:
                return "Valor de nodo 'Detalle' en sección 'OtrosCargos', línea " \
                       + str(position + 1) + " no posee un formato válido (máximo 160 caracteres, caracteres" \
                                             " recibidos: " + str(len(detailsNode)) + ")"
            else:
                return True
        except:
            return "Valor de nodo 'Detalle' en sección './/OtrosCargos, no puede ser vacío."
    else:
        return True


def validateOCPercent(data: xml.etree.ElementTree.Element, position):
    otherChargesNode = data.findall(".//OtrosCargos")
    if len(otherChargesNode) > 0:
        try:
            percentageNode = data.findall(".//OtrosCargos/Porcentaje")[position].text
            isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(percentageNode, 9, 5)
            if not isValidDecimal:
                return "Valor de nodo 'Porcentaje' en sección 'OtrosCargos', línea " \
                       + str(position + 1) + " no posee un formato válido (9 enteros (máximo), 5 decimales. Recibido: " \
                   + percentageNode + ")"
            else:
                return True
        except:
            return "Valor de nodo 'Porcentaje' en sección './/OtrosCargos, no puede ser vacío."
    else:
        return True


def validateChargeAmount(data: xml.etree.ElementTree.Element, position):
    otherChargesNode = data.findall(".//OtrosCargos")
    if len(otherChargesNode) > 0:
        try:
            chargeNode = data.findall(".//OtrosCargos/MontoCargo")[position].text
            isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(chargeNode, 18, 5)
            if not isValidDecimal:
                return "Valor de nodo 'MontoCargo' en sección 'OtrosCargos', línea " \
                       + str(position + 1) + " no posee un formato válido (18 enteros (máximo), 5 decimales. Recibido: " \
                   + chargeNode + ")"
            else:
                return True
        except:
            return "Valor de nodo 'MontoCargo' en sección './/OtrosCargos, no puede ser vacío."
    else:
        return True
