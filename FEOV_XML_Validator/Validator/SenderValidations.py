import xml.etree.ElementTree
import Validator.AuxiliarFunctions
import re

# Expresion regular que solo acepta numeros del 0 al 9.
REOnlyNumbers = "[0-9]+$"

# Namespace necesario al momento de obtener un nodo, sin esto no se pueden leer los datos del nodo.
namespaces = {'eInvoiceNameSpace': 'https://cdn.comprobanteselectronicos.go.cr/xml-schemas/v4.3/facturaElectronica'}

# Expresión regular para validar correos (explícitamente obtenida del esquema de hacienda en su versión 4.3)
REEmailSender = "^\\s*(([^<>()\\[\\]\\.,;:\\s@\\\"]+(\\.[^<>()\\[\\]\\.,;:\\s@\\\"]+)*)|(\\\".+\\\"))@(([^<>()\\[\\]\\.,;:\\s@\\\"]+\\.)+[^<>()\\[\\]\\.,;:\\s@\\\"]{0,})\\s*$"


def validateSenderInfo(data: xml.etree.ElementTree.Element):
    senderNode = data.find('eInvoiceNameSpace:Emisor', namespaces)
    results = [validateSenderNode(senderNode), validateSenderName(senderNode), validateSenderID(senderNode),
               validateSenderIDType(senderNode), validateSenderIDNum(senderNode),
               validateSenderCommercialName(senderNode), validateSenderLocation(senderNode),
               validateSenderState(senderNode), validateSenderCounty(senderNode), validateSenderCity(senderNode),
               validateSenderNeighborhood(senderNode), validateSenderOtherSigns(senderNode),
               validateSenderTelephone(senderNode), validateSenderFax(senderNode), validateSenderEmail(senderNode),
               validateSenderEmailDetail(senderNode)]
    formattedSenderResults = Validator.AuxiliarFunctions.flattenList(results)
    return formattedSenderResults


def validateSenderNode(senderNode):
    if senderNode:
        return True
    else:
        return "No existe Nodo de Emisor en XML"



def validateSenderName(senderNode):
    Name = senderNode.find('eInvoiceNameSpace:Nombre', namespaces).text
    if len(Name) == 0 or len(Name) > 100:
        return "-25, El nombre del Emisor no puede estar vacío ni exceder los 100 caracteres"
    else:
        return True


def validateSenderID(senderNode):
    IDNode = senderNode.find('eInvoiceNameSpace:Identificacion', namespaces)
    if IDNode:
        return True
    else:
        return "No se encuenta nodo de identificación de Emisor, el cual es de caracter obligatorio."


def validateSenderIDType(senderNode):
    acceptedIDTypes = ["01", "02", "03", "04"]
    idNode = senderNode.find('eInvoiceNameSpace:Identificacion', namespaces)
    IDNodeType = idNode.find('eInvoiceNameSpace:Tipo', namespaces).text
    if len(IDNodeType) == 0 or len(IDNodeType) > 2 or IDNodeType not in acceptedIDTypes:
        return "El valor '" + IDNodeType + "' del nodo 'Tipo' en la sección del Emisor, no es válido con respecto al" \
                                           " catálogo de tipos: " + str(acceptedIDTypes)
    else:
        return True


def validateSenderIDNum(senderNode):
    idNode = senderNode.find('eInvoiceNameSpace:Identificacion', namespaces)
    idNodeType = idNode.find('eInvoiceNameSpace:Tipo', namespaces).text
    idNumber = idNode.find('eInvoiceNameSpace:Numero', namespaces).text
    IdTypesCorrespondingFunctions = {
        "01": Validator.AuxiliarFunctions.validatePhysicalID,
        "02": Validator.AuxiliarFunctions.validateLegalID,
        "03": Validator.AuxiliarFunctions.validateDIMEXID,
        "04": Validator.AuxiliarFunctions.validateNITEID
    }
    try:
        chosen_operation_function = IdTypesCorrespondingFunctions.get(idNodeType,"Recibido tipo de identificación inválido")
        result = chosen_operation_function(idNumber)
        return result
    except:
        return "No es posible validar el ID del Emisor debido a su tipo."


def validateSenderCommercialName(senderNode):
    CommercialName = senderNode.find('eInvoiceNameSpace:NombreComercial', namespaces).text
    if len(CommercialName) > 80:
        return "Excedida cantidad límite de caracteres para nombre comercial de Emisor (Permitido : 80, recibido: " \
               + str(len(CommercialName)) + ")"
    else:
        return True


def validateSenderLocation(senderNode):
    LocationNode = senderNode.findall('eInvoiceNameSpace:Ubicacion', namespaces)
    if len(LocationNode) == 0:
        return "No existe Nodo de Ubicacion en XML"
    else:
        return True


# state county city
def validateSenderState(senderNode):  # Provincia
    LocationNode = senderNode.find('eInvoiceNameSpace:Ubicacion', namespaces)
    StateNode = LocationNode.find('eInvoiceNameSpace:Provincia', namespaces).text
    if len(StateNode) != 1 or StateNode.isnumeric() == False:
        return "El nodo de provincia del Emisor no posee la estructura correcta. Solo debe contener un único dígito y" \
               " debe ser un número. (Dato recibido: '" + str(StateNode) + "', número de dígitos: " + str(
            len(StateNode)) + ")"
    else:
        return True


def validateSenderCounty(senderNode):  # Canton
    LocationNode = senderNode.find('eInvoiceNameSpace:Ubicacion', namespaces)
    CountyNode = LocationNode.find('eInvoiceNameSpace:Canton', namespaces).text
    if len(CountyNode) != 2 or CountyNode.isnumeric() == False:
        return "El nodo de Canton del Emisor no posee la estructura correcta. Solo debe contener dos dígitos y" \
               " debe ser un número. (Dato recibido: '" + str(CountyNode) + "', número de dígitos: " + str(
            len(CountyNode)) + ")"
    else:
        return True


def validateSenderCity(senderNode):  # Distrito
    LocationNode = senderNode.find('eInvoiceNameSpace:Ubicacion', namespaces)
    CityNode = LocationNode.find('eInvoiceNameSpace:Distrito', namespaces).text
    if len(CityNode) != 2 or CityNode.isnumeric() == False:
        return "El nodo de Distrito del Emisor no posee la estructura correcta. Solo debe contener dos dígitos y" \
               " debe ser un número. (Dato recibido: '" + str(CityNode) + "', número de dígitos: " + str(
            len(CityNode)) + ")"
    else:
        return True


def validateSenderNeighborhood(senderNode):  # Barrio
    try:
        LocationNode = senderNode.find('eInvoiceNameSpace:Ubicacion', namespaces)
        NeighborhoodNode = LocationNode.find('eInvoiceNameSpace:Barrio', namespaces).text
        if len(NeighborhoodNode) != 2 or NeighborhoodNode.isnumeric() == False:
            return "El nodo de Barrio del Emisor no posee la estructura correcta. Solo debe contener dos dígitos y" \
                   " debe ser un número. (Dato recibido: '" + str(NeighborhoodNode) + "', número de dígitos: " + str(
                len(NeighborhoodNode)) + ")"
        else:
            return True
    except:
        return True


def validateSenderOtherSigns(senderNode):
    LocationNode = senderNode.find('eInvoiceNameSpace:Ubicacion', namespaces)
    OtherSignsNode = LocationNode.findall('eInvoiceNameSpace:OtrasSenas', namespaces)
    OtherSigns = LocationNode.find('eInvoiceNameSpace:OtrasSenas', namespaces).text
    if len(OtherSignsNode) == 0:
        return "No existe Nodo de Ubicacion en XML"
    else:
        if len(OtherSigns) > 250:
            return "Excedido límite de caractreres para nodo OtrasSenas de Emisor. (Permitido: 250. Recibido: " + str(
                len(OtherSigns[0].text)) + ")"
        else:
            return True


def validateSenderTelephone(senderNode):  # ***
    try:
        TelephoneNode = senderNode.find('eInvoiceNameSpace:Telefono', namespaces)
        telephoneResults = [validateSenderTelephoneCountryCode(TelephoneNode), validateSenderTelephoneNumber(TelephoneNode)]
        return telephoneResults
    except:
        return True


def validateSenderTelephoneCountryCode(TelephoneNode):
    CountryCode = TelephoneNode.find('eInvoiceNameSpace:CodigoPais', namespaces).text
    if re.match(REOnlyNumbers, CountryCode) == None or len(CountryCode) != 3:
        return "Formato de código páis de número de teléfono de Emisor no es válido. Solo se permite un máximo de" \
               " 3 Números. (Recibido: " + CountryCode + ")."
    else:
        return True


def validateSenderTelephoneNumber(TelephoneNode):
    telephoneNumber = TelephoneNode.find('eInvoiceNameSpace:NumTelefono', namespaces).text
    if re.match(REOnlyNumbers, telephoneNumber) == None or len(telephoneNumber) > 20:
        return "Formato de número telefónico de Emisor no es válido. Solo se permite un máximo de 20 números." \
               " (Recibido: " + str(telephoneNumber) + ")."
    else:
        return True


def validateSenderFax(senderNode):  # ***
    try:
        faxNode = senderNode.find('eInvoiceNameSpace:Fax', namespaces)
        faxResults = [validateSenderTelephoneCountryCode(faxNode), validateSenderTelephoneNumber(faxNode)]
        return faxResults
    except:
        return True


def validateSenderFaxCountryCode(faxNode):
    CountryCode = faxNode.find('eInvoiceNameSpace:CodigoPais', namespaces).text
    if re.match(REOnlyNumbers, CountryCode) == None or len(CountryCode) != 3:
        return "Formato de código páis de número de teléfono de Emisor no es válido. Solo se permite un máximo de" \
               " 3 Números. (Recibido: " + CountryCode + ")."
    else:
        return True


def validateSenderFaxNumber(faxNode):
    FaxNumber = faxNode.find('eInvoiceNameSpace:NumTelefono', namespaces).text
    if re.match(REOnlyNumbers, FaxNumber) == None or len(FaxNumber) > 20:
        return "Formato de número telefónico de Emisor no es válido. Solo se permite un máximo de 20 números." \
               " (Recibido: " + str(FaxNumber) + ")."
    else:
        return True


def validateSenderEmail(senderNode):
    EmailNode = senderNode.findall('eInvoiceNameSpace:CorreoElectronico', namespaces)
    if len(EmailNode) == 0:
        return "No se encuenta nodo de Correo Electronico de Emisor, el cual es de caracter obligatorio."
    else:
        return True


def validateSenderEmailDetail(senderNode):
    EmailNode = senderNode.find('eInvoiceNameSpace:CorreoElectronico', namespaces).text
    if re.match(REEmailSender, EmailNode) == None or len(EmailNode) > 160:
        return "Formato de Correo Electronico de Emisor no es válido. (Recibido: " + EmailNode + ")"
    else:
        return True

