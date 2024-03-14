import xml.etree.ElementTree
import XMLValidator.Validator.AuxiliarFunctions as AuxiliarFunctions
import re

# Expresion regular que solo acepta numeros del 0 al 9.
REOnlyNumbers = "[0-9]+$"

# Namespace necesario al momento de obtener un nodo, sin esto no se pueden leer los datos del nodo.
namespaces = {'eInvoiceNameSpace': 'https://cdn.comprobanteselectronicos.go.cr/xml-schemas/v4.3/facturaElectronicaCompra'}

# Expresión regular para validar correos (explícitamente obtenida del esquema de hacienda en su versión 4.3)
REEmailReceiver = "^\\s*(([^<>()\\[\\]\\.,;:\\s@\\\"]+(\\.[^<>()\\[\\]\\.,;:\\s@\\\"]+)*)|(\\\".+\\\"))@(([^<>()\\[\\]\\.,;:\\s@\\\"]+\\.)+[^<>()\\[\\]\\.,;:\\s@\\\"]{0,})\\s*$"


def validateReceiverInfo(data):
    receiverNode = data.find('eInvoiceNameSpace:Receptor', namespaces)
    results = [validateReceiverNode(receiverNode), validateReceiverName(receiverNode), validateReceiverID(receiverNode),
               validateReceiverIDType(receiverNode), validateReceiverIDNum(receiverNode),
               validateReceiverCommercialName(receiverNode), validateReceiverLocation(receiverNode),
               validateReceiverState(receiverNode), validateReceiverCounty(receiverNode),
               validateReceiverCity(receiverNode), validateReceiverNeighborhood(receiverNode),
               validateReceiverOtherSigns(receiverNode), validateReceiverTelephone(receiverNode),
               validateReceiverFax(receiverNode), validateReceiverEmail(receiverNode),
               validateReceiverEmailDetail(receiverNode)]
    formattedReceiverResults = AuxiliarFunctions.flattenList(results)
    return formattedReceiverResults

def validateReceiverNode(receiverNode):
    if receiverNode:
        return True
    else:
        return "No existe Nodo de Receptor en XML"


def validateReceiverName(receiverNode):
    try:
        Name = receiverNode.find('eInvoiceNameSpace:Nombre', namespaces).text
        if len(Name) == 0 or len(Name) > 100:
            return "-25, El nombre del Receptor no puede estar vacío ni exceder los 100 caracteres"
        else:
            return True
    except:
        return "Nodo 'Nombre' de sección de Receptor no puede ser vacío."

def validateReceiverID(receiverNode):
    IDNode = receiverNode.findall('eInvoiceNameSpace:Identificacion', namespaces)
    if len(IDNode) == 0:
        return "No se encuenta nodo de identificación de Receptor, el cual es de caracter olbigatorio."
    else:
        return True


def validateReceiverIDType(receiverNode):
    acceptedIDTypes = ["01", "02", "03", "04"]
    IDNode = receiverNode.find('eInvoiceNameSpace:Identificacion', namespaces)
    if IDNode == None:
        return "Factura no posee nodo 'Identificacion', por lo que no se puede evaluar el tipo de identificación."
    try:
        IDNodeType = IDNode.find('eInvoiceNameSpace:Tipo', namespaces).text
        if len(IDNodeType) == 0 or len(IDNodeType) > 2 or IDNodeType not in acceptedIDTypes:
            return "El valor '" + IDNodeType + "' del nodo 'Tipo' en la sección del Receptor, no es válido con respecto " \
                   "al catálogo de tipos aceptados: " + str(acceptedIDTypes)
        else:
            return True
    except:
        return "Nodo 'Tipo' en sección Receptor/Identificacion no puede ser vacío."



def validateReceiverIDNum(receiverNode):
    IDNode = receiverNode.find('eInvoiceNameSpace:Identificacion', namespaces)
    IDNodeType = IDNode.find('eInvoiceNameSpace:Tipo', namespaces).text
    IDNodeNumber = IDNode.find('eInvoiceNameSpace:Numero', namespaces).text
    IdTypesCorrespondingFunctions = {
        "01": AuxiliarFunctions.validatePhysicalIDRec,
        "02": AuxiliarFunctions.validateLegalIDRec,
        "03": AuxiliarFunctions.validateDIMEXIDRec,
        "04": AuxiliarFunctions.validateNITEIDRec
    }
    try:
        chosen_operation_function = IdTypesCorrespondingFunctions.get(IDNodeType,
                                                                      "Recibido tipo de identificación inválido")
        result = chosen_operation_function(IDNodeNumber)
        return result
    except:
        return "No es posible validar el ID del Receptor debido a su tipo o por tener nodo 'Numero' vacío."


def validateReceiverCommercialName(receiverNode):
    try:
        CommercialNameNode = receiverNode.find('eInvoiceNameSpace:NombreComercial', namespaces).text
        if len(CommercialNameNode) > 80:
            return "Excedida cantidad límite de caracteres para nombre comercial de Receptor (Permitido : 80, recibido: " \
                   + str(len(CommercialNameNode)) + ")"
        else:
            return True
    except:
        return "Nodo 'NombreComercial' en sección de Receptor no puede ser vacío."

def validateReceiverLocation(receiverNode):
    LocationNode = receiverNode.findall('eInvoiceNameSpace:Ubicacion', namespaces)
    if len(LocationNode) == 0:
        return "No existe Nodo de Ubicacion en XML"
    else:
        return True


# state county city
def validateReceiverState(receiverNode):  # Provincia
    LocationNode = receiverNode.find('eInvoiceNameSpace:Ubicacion', namespaces)
    try:
        StateNode = LocationNode.find('eInvoiceNameSpace:Provincia', namespaces).text
        if len(StateNode) != 1 or StateNode.isnumeric() == False:
            return "El nodo de provincia del Receptor no posee la estructura correcta. Solo debe contener un único dígito y" \
                   " debe ser un número. (Dato recibido: '" + str(StateNode) + "', número de dígitos: " + str(len(StateNode)) + ")"
        else:
            return True
    except:
        return "Nodo 'Provincia' en sección de Receptor no puede ser vacío."

def validateReceiverCounty(receiverNode):  # Canton
    LocationNode = receiverNode.find('eInvoiceNameSpace:Ubicacion', namespaces)
    try:
        CountyNode = LocationNode.find('eInvoiceNameSpace:Canton', namespaces).text
        if len(CountyNode) != 2 or CountyNode.isnumeric() == False:
            return "El nodo de Canton del Receptor no posee la estructura correcta. Solo debe contener dos dígitos y" \
                   " debe ser un número. (Dato recibido: '" + str(CountyNode) + "', número de dígitos: " + str(len(CountyNode)) + ")"
        else:
            return True
    except:
        return "Nodo 'Canton' en sección de Receptor no puede ser vacío."

def validateReceiverCity(receiverNode):  # Distrito
    LocationNode = receiverNode.find('eInvoiceNameSpace:Ubicacion', namespaces)
    try:
        CityNode = LocationNode.find('eInvoiceNameSpace:Distrito', namespaces).text
        if len(CityNode) != 2 or CityNode.isnumeric() == False:
            return "El nodo de Distrito del Receptor no posee la estructura correcta. Solo debe contener dos dígitos y" \
                   " debe ser un número. (Dato recibido: '" + str(CityNode) + "', número de dígitos: " + str(len(CityNode)) + ")"
        else:
            return True
    except:
        return "Nodo 'Distrito' en sección de Receptor no puede ser vacío."

def validateReceiverNeighborhood(receiverNode):  # Barrio
    try:
        LocationNode = receiverNode.find('eInvoiceNameSpace:Ubicacion', namespaces)
        NeighborhoodNode = LocationNode.find('eInvoiceNameSpace:Barrio', namespaces).text
        if len(NeighborhoodNode) != 2 or NeighborhoodNode.isnumeric() == False:
            return "El nodo de Barrio del Receptor no posee la estructura correcta. Solo debe contener dos dígitos y" \
                   " debe ser un número. (Dato recibido: '" + str(NeighborhoodNode) + "', número de dígitos: " + str(len(NeighborhoodNode)) + ")"
        else:
            return True
    except:
        return True


def validateReceiverOtherSigns(receiverNode):
    LocationNode = receiverNode.find('eInvoiceNameSpace:Ubicacion', namespaces)
    try:
        OtherSigns = LocationNode.find('eInvoiceNameSpace:OtrasSenas', namespaces).text
        if len(OtherSigns) > 250:
            return "Excedido límite de caractreres para nodo OtrasSenas de Receptor. (Permitido: 250. Recibido: " + str(
                len(OtherSigns)) + ")"
        else:
            return True
    except:
        return "Nodo 'OtrasSenas' en sección de Receptor no puede ser vacío."

def validateReceiverTelephone(receiverNode):  # ***
    try:
        phoneNode = receiverNode.find('eInvoiceNameSpace:Telefono', namespaces)
        if phoneNode != None:
            telephoneResults = [validateReceiverTelephoneCountryCode(phoneNode), validateReceiverTelephoneNumber(phoneNode)]
            return telephoneResults
        else:
            return True
    except:
        return True


def validateReceiverTelephoneCountryCode(phoneNode):
    try:
        CountryCode = phoneNode.find('eInvoiceNameSpace:CodigoPais', namespaces).text
        if re.match(REOnlyNumbers, CountryCode) == None or len(CountryCode) != 3:
            return "Formato de código páis de número de teléfono de Receptor no es válido. Solo se permite un máximo de" \
                   " 3 Números. (Recibido: " + CountryCode + ")."
        else:
            return True
    except:
        return "Nodo 'CodigoPais' en sección Receptor/Telefono no puede ser vacío."

def validateReceiverTelephoneNumber(phoneNode):
    try:
        telephoneNumber = phoneNode.find('eInvoiceNameSpace:NumTelefono', namespaces).text
        if re.match(REOnlyNumbers, telephoneNumber) == None or len(telephoneNumber) > 20:
            return "Formato de número telefónico de Receptor no es válido. Solo se permite un máximo de 20 números." \
                   " (Recibido: " + str(telephoneNumber) + ")."
        else:
            return True
    except:
        return "Nodo 'NumTelefono' en sección Receptor/Telefono no puede ser vacío."

def validateReceiverFax(receiverNode):  # ***
    try:
        FaxNode = receiverNode.find('eInvoiceNameSpace:Fax', namespaces)
        if FaxNode != None:
            faxResults = [validateReceiverFaxCountryCode(FaxNode), validateReceiverFaxNumber(FaxNode)]
            return faxResults
        else:
            return True
    except:
        return True


def validateReceiverFaxCountryCode(receiverNode):
    try:
        CountryCode = receiverNode.find('eInvoiceNameSpace:CodigoPais', namespaces).text
        if re.match(REOnlyNumbers, CountryCode) == False or len(CountryCode) != 3:
            return "Formato de código páis de número de teléfono de Receptor no es válido. Solo se permite un máximo de" \
                   " 3 Números. (Recibido: " + CountryCode + ")."
        else:
            return True
    except:
        return "Nodo 'CodigoPais' en sección Receptor/Fax no puede ser vacío."

def validateReceiverFaxNumber(receiverNode):
    try:
        FaxNumber = receiverNode.find('eInvoiceNameSpace:NumTelefono', namespaces).text
        if re.match(REOnlyNumbers, FaxNumber) == None or len(FaxNumber) > 20:
            return "Formato de número telefónico de Receptor no es válido. Solo se permite un máximo de 20 números." \
                   " (Recibido: " + str(FaxNumber) + ")."
        else:
            return True
    except:
        return "Nodo 'NumTelefono' en sección Receptor/Fax no puede ser vacío."

def validateReceiverEmail(receiverNode):
    EmailNode = receiverNode.findall('eInvoiceNameSpace:CorreoElectronico', namespaces)
    if len(EmailNode) == 0:
        return "No se encuenta nodo de Correo Electronico de Receptor, el cual es de caracter olbigatorio."
    else:
        return True


def validateReceiverEmailDetail(receiverNode):
    try:
        EmailNode = receiverNode.find('eInvoiceNameSpace:CorreoElectronico', namespaces).text
        if re.match(REEmailReceiver, EmailNode) == None or len(EmailNode) > 160:
            return "Formato de Correo Electronico de Receptor no es válido. (Recibido: " + EmailNode + ")"
        else:
            return True
    except:
        return "Nodo 'CorreoElectronico' en sección de Receptor no puede ser vacío."
