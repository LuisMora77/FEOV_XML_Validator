import xml.etree.ElementTree
import Validator.AuxiliarFunctions
import re

# Expresion regular que solo acepta numeros del 0 al 9.
REOnlyNumbers = "[0-9]+$"

# Expresión regular para validar correos (explícitamente obtenida del esquema de hacienda en su versión 4.3)
REEmailSender = "^\\s*(([^<>()\\[\\]\\.,;:\\s@\\\"]+(\\.[^<>()\\[\\]\\.,;:\\s@\\\"]+)*)|(\\\".+\\\"))@(([^<>()\\[\\]\\.,;:\\s@\\\"]+\\.)+[^<>()\\[\\]\\.,;:\\s@\\\"]{0,})\\s*$"


def validateSenderInfo(data: xml.etree.ElementTree.Element):
    results = [validateSenderNode(data), validateSenderName(data), validateSenderID(data), validateSenderIDType(data),
               validateSenderIDNum(data), validateSenderCommercialName(data), validateSenderLocation(data),
               validateSenderState(data), validateSenderCounty(data), validateSenderCity(data),
               validateSenderNeighborhood(data), validateSenderOtherSigns(data), validateSenderTelephone(data),
               validateSenderFax(data), validateSenderEmail(data), validateSenderEmailDetail(data)]
    return results


def validateSenderNode(data: xml.etree.ElementTree.Element):
    EmisorNode = data.findall("Emisor")
    if len(EmisorNode) == 0:
        return "No existe Nodo de Emisor en XML"
    else:
        return True


def validateSenderName(data: xml.etree.ElementTree.Element):
    Name = data.findall('.//Emisor/Nombre')[0].text
    if len(Name) == 0 or len(Name) > 100:
        return "-25, El nombre del Emisor no puede estar vacío ni exceder los 100 caracteres"
    else:
        return True


def validateSenderID(data: xml.etree.ElementTree.Element):
    IDNode = data.findall('.//Emisor/Identificacion')
    if len(IDNode) == 0:
        return "No se encuenta nodo de identificación de Emisor, el cual es de caracter obligatorio."
    else:
        return True


def validateSenderIDType(data: xml.etree.ElementTree.Element):
    acceptedIDTypes = ["01", "02", "03", "04"]
    IDNodeType = data.findall('.//Emisor/Identificacion/Tipo')[0].text
    if len(IDNodeType) == 0 or len(IDNodeType) > 2:
        return "Tipo de cédula de Emisor no posee el formato adecuado"
    if IDNodeType in acceptedIDTypes:
        return True
    else:
        return "El valor (" + IDNodeType + ") del nodo 'Tipo' en la sección del Emisor, no es válido con respecto al" \
                                           " catálogo de tipos: " + str(acceptedIDTypes)


def validateSenderIDNum(data: xml.etree.ElementTree.Element):
    IDNodeType = data.findall('.//Emisor/Identificacion/Tipo')[0].text
    IDNumber = data.findall('.//Emisor/Identificacion/Numero')[0].text
    IdTypesCorrespondingFunctions = {
        "01": Validator.AuxiliarFunctions.validatePhysicalID,
        "02": Validator.AuxiliarFunctions.validateLegalID,
        "03": Validator.AuxiliarFunctions.validateDIMEXID,
        "04": Validator.AuxiliarFunctions.validateNITEID
    }
    try:
        chosen_operation_function = IdTypesCorrespondingFunctions.get(IDNodeType,
                                                                      "Recibido tipo de identificación inválido")
        result = chosen_operation_function(IDNumber)
        return result
    except:
        return "No es posible validar el ID del Emisor debido a su tipo."


def validateSenderCommercialName(data: xml.etree.ElementTree.Element):
    CommercialNameNode = data.findall('.//Emisor/NombreComercial')[0].text
    if len(CommercialNameNode) > 80:
        return "Excedida cantidad límite de caracteres para nombre comercial de Emisor (Permitido : 80, recibido: " \
               + str(len(CommercialNameNode)) + ")"
    else:
        return True


def validateSenderLocation(data: xml.etree.ElementTree.Element):
    LocationNode = data.findall('.//Emisor/Ubicacion')
    if len(LocationNode) == 0:
        return "No existe Nodo de Ubicacion en XML"
    else:
        return True


# state county city
def validateSenderState(data: xml.etree.ElementTree.Element):  # Provincia
    StateNode = data.findall('.//Emisor/Ubicacion/Provincia')[0].text
    if len(StateNode) != 1 or StateNode.isnumeric() == False:
        return "El nodo de provincia del Emisor no posee la estructura correcta. Solo debe contener un único dígito y" \
               " debe ser un número. (Dato recibido: '" + str(StateNode) + "', número de dígitos: " + str(
            len(StateNode)) + ")"
    else:
        return True


def validateSenderCounty(data: xml.etree.ElementTree.Element):  # Canton
    CountyNode = data.findall('.//Emisor/Ubicacion/Canton')[0].text
    if len(CountyNode) != 2 or CountyNode.isnumeric() == False:
        return "El nodo de Canton del Emisor no posee la estructura correcta. Solo debe contener dos dígitos y" \
               " debe ser un número. (Dato recibido: '" + str(CountyNode) + "', número de dígitos: " + str(
            len(CountyNode)) + ")"
    else:
        return True


def validateSenderCity(data: xml.etree.ElementTree.Element):  # Distrito
    CityNode = data.findall('.//Emisor/Ubicacion/Distrito')[0].text
    if len(CityNode) != 2 or CityNode.isnumeric() == False:
        return "El nodo de Distrito del Emisor no posee la estructura correcta. Solo debe contener dos dígitos y" \
               " debe ser un número. (Dato recibido: '" + str(CityNode) + "', número de dígitos: " + str(
            len(CityNode)) + ")"
    else:
        return True


def validateSenderNeighborhood(data: xml.etree.ElementTree.Element):  # Barrio
    try:
        NeighborhoodNode = data.findall('.//Emisor/Ubicacion/Barrio')[0].text
        if len(NeighborhoodNode) != 2 or NeighborhoodNode.isnumeric() == False:
            return "El nodo de Barrio del Emisor no posee la estructura correcta. Solo debe contener dos dígitos y" \
                   " debe ser un número. (Dato recibido: '" + str(NeighborhoodNode) + "', número de dígitos: " + str(
                len(NeighborhoodNode)) + ")"
        else:
            return True
    except:
        return True


def validateSenderOtherSigns(data: xml.etree.ElementTree.Element):
    OtherSigns = data.findall('.//Emisor/Ubicacion/OtrasSenas')
    if len(OtherSigns) == 0:
        return "No existe Nodo de Ubicacion en XML"
    else:
        if len(OtherSigns[0].text) > 250:
            return "Excedido límite de caractreres para nodo OtrasSenas de Emisor. (Permitido: 250. Recibido: " + str(
                len(OtherSigns[0].text)) + ")"
        else:
            return True


def validateSenderTelephone(data: xml.etree.ElementTree.Element):  # ***
    try:
        data.findall('.//Emisor/Telefono')
        telephoneResults = [validateSenderTelephoneCountryCode(data), validateSenderTelephoneNumber(data)]
        return telephoneResults
    except:
        return True


def validateSenderTelephoneCountryCode(data: xml.etree.ElementTree.Element):
    CountryCode = data.findall('.//Emisor/Telefono/CodigoPais')[0].text
    if re.match(REOnlyNumbers, CountryCode) == None or len(CountryCode) != 3:
        return "Formato de código páis de número de teléfono de Emisor no es válido. Solo se permite un máximo de" \
               " 3 Números. (Recibido: " + CountryCode + ")."
    else:
        return True


def validateSenderTelephoneNumber(data: xml.etree.ElementTree.Element):
    telephoneNumber = data.findall('.//Emisor/Telefono/NumTelefono')[0].text
    if re.match(REOnlyNumbers, telephoneNumber) == None or len(telephoneNumber) > 20:
        return "Formato de número telefónico de Emisor no es válido. Solo se permite un máximo de 20 números." \
               " (Recibido: " + str(telephoneNumber) + ")."
    else:
        return True


def validateSenderFax(data: xml.etree.ElementTree.Element):  # ***
    try:
        data.findall('.//Emisor/Fax')
        faxResults = [validateSenderTelephoneCountryCode(data), validateSenderTelephoneNumber(data)]
        return faxResults
    except:
        return True


def validateSenderFaxCountryCode(data: xml.etree.ElementTree.Element):
    CountryCode = data.findall('.//Emisor/Fax/CodigoPais')[0].text
    if re.match(REOnlyNumbers, CountryCode) == None or len(CountryCode) != 3:
        return "Formato de código páis de número de teléfono de Emisor no es válido. Solo se permite un máximo de" \
               " 3 Números. (Recibido: " + CountryCode + ")."
    else:
        return True


def validateSenderFaxNumber(data: xml.etree.ElementTree.Element):
    FaxNumber = data.findall('.//Emisor/Fax/NumTelefono')[0].text
    if re.match(REOnlyNumbers, FaxNumber) == None or len(FaxNumber) > 20:
        return "Formato de número telefónico de Emisor no es válido. Solo se permite un máximo de 20 números." \
               " (Recibido: " + str(FaxNumber) + ")."
    else:
        return True


def validateSenderEmail(data: xml.etree.ElementTree.Element):
    EmailNode = data.findall('.//Emisor/CorreoElectronico')
    if len(EmailNode) == 0:
        return "No se encuenta nodo de Correo Electronico de Emisor, el cual es de caracter obligatorio."
    else:
        return True


def validateSenderEmailDetail(data: xml.etree.ElementTree.Element):
    EmailNode = data.findall('.//Emisor/CorreoElectronico')[0].text
    if re.match(REEmailSender, EmailNode) == None or len(EmailNode) > 160:
        return "Formato de Correo Electronico de Emisor no es válido. (Recibido: " + EmailNode + ")"
    else:
        return True

# def validateSubNodes(root,ParentNodeName):
#    ParentNodePath = './/' + ParentNodeName +  '/*'
#    childTags = [t.tag for t in root.findall(ParentNodePath)]
#    for childNode in childTags:
#        print("ChildNode: " + childNode)
