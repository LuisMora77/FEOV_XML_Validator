import xml.etree.ElementTree
import XMLValidator.Validator.AuxiliarFunctions as AuxiliarFunctions
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
    formattedSenderResults = AuxiliarFunctions.flattenList(results)
    return formattedSenderResults


def validateSenderNode(senderNode):
    if senderNode:
        return True
    else:
        return "No existe Nodo de Emisor en XML"



def validateSenderName(senderNode):
    try:
        Name = senderNode.find('eInvoiceNameSpace:Nombre', namespaces).text
        if len(Name) == 0 or len(Name) > 100:
            return "-25, El nombre del Emisor no puede estar vacío ni exceder los 100 caracteres"
        else:
            return True
    except:
        return "Nodo 'Nombre' de sección de Emisor no puede ser vacío."


def validateSenderID(senderNode):
    IDNode = senderNode.find('eInvoiceNameSpace:Identificacion', namespaces)
    if IDNode:
        return True
    else:
        return "No se encuenta nodo de identificación de Emisor, el cual es de caracter obligatorio."


def validateSenderIDType(senderNode):
    acceptedIDTypes = ["01", "02", "03", "04"]
    idNode = senderNode.find('eInvoiceNameSpace:Identificacion', namespaces)
    if idNode == None:
        return "Factura no posee nodo 'Identificacion', por lo que no se puede evaluar el tipo de identificación."
    try:
        IDNodeType = idNode.find('eInvoiceNameSpace:Tipo', namespaces).text
        if len(IDNodeType) == 0 or len(IDNodeType) > 2 or IDNodeType not in acceptedIDTypes:
            return "El valor '" + IDNodeType + "' del nodo 'Tipo' en la sección del Emisor, no es válido con respecto al" \
                                           " catálogo de tipos: " + str(acceptedIDTypes)
        else:
            return True
    except:
        return "Nodo 'Tipo' en sección Emisor/Identificacion no puede ser vacío."


def validateSenderIDNum(senderNode):
    idNode = senderNode.find('eInvoiceNameSpace:Identificacion', namespaces)
    idNodeType = idNode.find('eInvoiceNameSpace:Tipo', namespaces).text
    idNumber = idNode.find('eInvoiceNameSpace:Numero', namespaces).text
    IdTypesCorrespondingFunctions = {
        "01": AuxiliarFunctions.validatePhysicalID,
        "02": AuxiliarFunctions.validateLegalID,
        "03": AuxiliarFunctions.validateDIMEXID,
        "04": AuxiliarFunctions.validateNITEID
    }
    try:
        chosen_operation_function = IdTypesCorrespondingFunctions.get(idNodeType,"Recibido tipo de identificación inválido")
        result = chosen_operation_function(idNumber)
        return result
    except:
        return "No es posible validar el ID del Emisor debido a su tipo o por tener nodo 'Numero' vacío."


def validateSenderCommercialName(senderNode):
    try:
        CommercialName = senderNode.find('eInvoiceNameSpace:NombreComercial', namespaces).text
        if len(CommercialName) > 80:
            return "Excedida cantidad límite de caracteres para nombre comercial de Emisor (Permitido : 80, recibido: " \
               + str(len(CommercialName)) + ")"
        else:
            return True
    except:
        return "Nodo 'NombreComercial' en sección de Emisor no puede ser vacío."

def validateSenderLocation(senderNode):
    LocationNode = senderNode.findall('eInvoiceNameSpace:Ubicacion', namespaces)
    if len(LocationNode) == 0:
        return "No existe Nodo de Ubicacion en XML"
    else:
        return True


# state county city
def validateSenderState(senderNode):  # Provincia
    LocationNode = senderNode.find('eInvoiceNameSpace:Ubicacion', namespaces)
    try:
        StateNode = LocationNode.find('eInvoiceNameSpace:Provincia', namespaces).text
        if len(StateNode) != 1 or StateNode.isnumeric() == False:
            return "El nodo de provincia del Emisor no posee la estructura correcta. Solo debe contener un único dígito y" \
               " debe ser un número. (Dato recibido: '" + str(StateNode) + "', número de dígitos: " + str(
                len(StateNode)) + ")"
        else:
            return True
    except:
        return "Nodo 'Provincia' en sección de Emisor no puede ser vacío."

def validateSenderCounty(senderNode):  # Canton
    LocationNode = senderNode.find('eInvoiceNameSpace:Ubicacion', namespaces)
    CountyNode = LocationNode.find('eInvoiceNameSpace:Canton', namespaces).text
    try:
        if len(CountyNode) != 2 or CountyNode.isnumeric() == False:
            return "El nodo de Canton del Emisor no posee la estructura correcta. Solo debe contener dos dígitos y" \
               " debe ser un número. (Dato recibido: '" + str(CountyNode) + "', número de dígitos: " + str(
                len(CountyNode)) + ")"
        else:
            return True
    except:
        return "Nodo 'Canton' en sección de Emisor no puede ser vacío."


def validateSenderCity(senderNode):  # Distrito
    LocationNode = senderNode.find('eInvoiceNameSpace:Ubicacion', namespaces)
    try:
        CityNode = LocationNode.find('eInvoiceNameSpace:Distrito', namespaces).text
        if len(CityNode) != 2 or CityNode.isnumeric() == False:
            return "El nodo de Distrito del Emisor no posee la estructura correcta. Solo debe contener dos dígitos y" \
               " debe ser un número. (Dato recibido: '" + str(CityNode) + "', número de dígitos: " + str(
                len(CityNode)) + ")"
        else:
            return True
    except:
        return "Nodo 'Distrito' en sección de Emisor no puede ser vacío."

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
    try:
        OtherSigns = LocationNode.find('eInvoiceNameSpace:OtrasSenas', namespaces).text
        if len(OtherSigns) > 250:
            return "Excedido límite de caractreres para nodo OtrasSenas de Emisor. (Permitido: 250. Recibido: " + str(
                len(OtherSigns)) + ")"
        else:
            return True
    except:
        return "Nodo 'OtrasSenas' en sección de Emisor no puede ser vacío."


def validateSenderTelephone(senderNode):  # ***
    try:
        TelephoneNode = senderNode.find('eInvoiceNameSpace:Telefono', namespaces)
        if TelephoneNode != None:
            telephoneResults = [validateSenderTelephoneCountryCode(TelephoneNode),
                                validateSenderTelephoneNumber(TelephoneNode)]
            return telephoneResults
        else:
            return True
    except:
        return True


def validateSenderTelephoneCountryCode(TelephoneNode):
    try:
        CountryCode = TelephoneNode.find('eInvoiceNameSpace:CodigoPais', namespaces).text
        if re.match(REOnlyNumbers, CountryCode) == None or len(CountryCode) != 3:
            return "Formato de código páis de número de teléfono de Emisor no es válido. Solo se permite un máximo de" \
                   " 3 Números. (Recibido: " + CountryCode + ")."
        else:
            return True
    except:
        return "Nodo 'CodigoPais' en sección Emisor/Telefono no puede ser vacío."

def validateSenderTelephoneNumber(TelephoneNode):
    try:
        telephoneNumber = TelephoneNode.find('eInvoiceNameSpace:NumTelefono', namespaces).text
        if re.match(REOnlyNumbers, telephoneNumber) == None or len(telephoneNumber) > 20:
            return "Formato de número telefónico de Emisor no es válido. Solo se permite un máximo de 20 números." \
                   " (Recibido: " + str(telephoneNumber) + ")."
        else:
            return True
    except:
        return "Nodo 'NumTelefono' en sección Emisor/Telefono no puede ser vacío."


def validateSenderFax(senderNode):  # ***
    try:
        faxNode = senderNode.find('eInvoiceNameSpace:Fax', namespaces)
        if(faxNode) != None:
            faxResults = [validateSenderFaxCountryCode(faxNode), validateSenderFaxNumber(faxNode)]
            return faxResults
        else:
            return True
    except:
        return True


def validateSenderFaxCountryCode(faxNode):
    try:
        CountryCode = faxNode.find('eInvoiceNameSpace:CodigoPais', namespaces).text
        if re.match(REOnlyNumbers, CountryCode) == None or len(CountryCode) != 3:
            return "Formato de código páis de número de teléfono de Emisor no es válido. Solo se permite un máximo de" \
                   " 3 Números. (Recibido: " + CountryCode + ")."
        else:
            return True
    except:
        return "Nodo 'CodigoPais' en sección Emisor/Fax no puede ser vacío."


def validateSenderFaxNumber(faxNode):
    try:
        FaxNumber = faxNode.find('eInvoiceNameSpace:NumTelefono', namespaces).text
        if re.match(REOnlyNumbers, FaxNumber) == None or len(FaxNumber) > 20:
            return "Formato de número telefónico de Emisor no es válido. Solo se permite un máximo de 20 números." \
                   " (Recibido: " + str(FaxNumber) + ")."
        else:
            return True
    except:
        return "Nodo 'NumTelefono' en sección Emisor/Fax no puede ser vacío."


def validateSenderEmail(senderNode):
    EmailNode = senderNode.findall('eInvoiceNameSpace:CorreoElectronico', namespaces)
    if len(EmailNode) == 0:
        return "No se encuenta nodo de Correo Electronico de Emisor, el cual es de caracter obligatorio."
    else:
        return True


def validateSenderEmailDetail(senderNode):
    try:
        EmailNode = senderNode.find('eInvoiceNameSpace:CorreoElectronico', namespaces).text
        if re.match(REEmailSender, EmailNode) == None or len(EmailNode) > 160:
            return "Formato de Correo Electronico de Emisor no es válido. (Recibido: " + EmailNode + ")"
        else:
            return True
    except:
        return "Nodo 'CorreoElectronico' en sección de Emisor no puede ser vacío."
