import xml.etree.ElementTree
import Validator.AuxiliarFunctions
import re

# Expresion regular que solo acepta numeros del 0 al 9.
REOnlyNumbers = "[0-9]+$"

# Expresión regular para validar correos (explícitamente obtenida del esquema de hacienda en su versión 4.3)
REEmailReceiver = "^\\s*(([^<>()\\[\\]\\.,;:\\s@\\\"]+(\\.[^<>()\\[\\]\\.,;:\\s@\\\"]+)*)|(\\\".+\\\"))@(([^<>()\\[\\]\\.,;:\\s@\\\"]+\\.)+[^<>()\\[\\]\\.,;:\\s@\\\"]{0,})\\s*$"


def validateReceiverInfo(data: xml.etree.ElementTree.Element):
    results = [validateReceiverNode(data), validateReceiverName(data), validateReceiverID(data), validateReceiverIDType(data),
               validateReceiverIDNum(data), validateReceiverCommercialName(data), validateReceiverLocation(data),
               validateReceiverState(data), validateReceiverCounty(data), validateReceiverCity(data),
               validateReceiverNeighborhood(data), validateReceiverOtherSigns(data), validateReceiverTelephone(data),
               validateReceiverFax(data), validateReceiverEmail(data), validateReceiverEmailDetail(data)]
    return results


def validateReceiverNode(data: xml.etree.ElementTree.Element):
    ReceptorNode = data.findall("Receptor")
    if len(ReceptorNode) == 0:
        return "No existe Nodo de Receptor en XML"
    else:
        return True


def validateReceiverName(data: xml.etree.ElementTree.Element):
    Name = data.findall('.//Receptor/Nombre')[0].text
    if len(Name) == 0 or len(Name) > 100:
        return "-25, El nombre del Receptor no puede estar vacío ni exceder los 100 caracteres"
    else:
        return True


def validateReceiverID(data: xml.etree.ElementTree.Element):
    IDNode = data.findall('.//Receptor/Identificacion')
    if len(IDNode) == 0:
        return "No se encuenta nodo de identificación de Receptor, el cual es de caracter olbigatorio."
    else:
        return True


def validateReceiverIDType(data: xml.etree.ElementTree.Element):
    acceptedIDTypes = ["01", "02", "03", "04"]
    IDNodeType = data.findall('.//Receptor/Identificacion/Tipo')[0].text
    if len(IDNodeType) == 0 or len(IDNodeType) > 2:
        return "Tipo de cédula de Receptor no posee el formato adecuado"
    if IDNodeType in acceptedIDTypes:
        return True
    else:
        return "El valor (" + IDNodeType + ") del nodo 'Tipo' en la sección del Receptor, no es válido con respecto al" \
                                           " catálogo de tipos: " + str(acceptedIDTypes)


def validateReceiverIDNum(data: xml.etree.ElementTree.Element):
    IDNodeType = data.findall('.//Receptor/Identificacion/Tipo')[0].text
    IDNumber = data.findall('.//Receptor/Identificacion/Numero')[0].text
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
        return "No es posible validar el ID del Receptor debido a su tipo."


def validateReceiverCommercialName(data: xml.etree.ElementTree.Element):
    CommercialNameNode = data.findall('.//Receptor/NombreComercial')[0].text
    if len(CommercialNameNode) > 80:
        return "Excedida cantidad límite de caracteres para nombre comercial de Receptor (Permitido : 80, recibido: " \
               + str(len(CommercialNameNode)) + ")"
    else:
        return True


def validateReceiverLocation(data: xml.etree.ElementTree.Element):
    LocationNode = data.findall('.//Receptor/Ubicacion')
    if len(LocationNode) == 0:
        return "No existe Nodo de Ubicacion en XML"
    else:
        return True


# state county city
def validateReceiverState(data: xml.etree.ElementTree.Element):  # Provincia
    StateNode = data.findall('.//Receptor/Ubicacion/Provincia')[0].text
    if len(StateNode) != 1 or StateNode.isnumeric() == False:
        return "El nodo de provincia del Receptor no posee la estructura correcta. Solo debe contener un único dígito y" \
               " debe ser un número. (Dato recibido: '" + str(StateNode) + "', número de dígitos: " + str(len(StateNode)) + ")"
    else:
        return True


def validateReceiverCounty(data: xml.etree.ElementTree.Element):  # Canton
    CountyNode = data.findall('.//Receptor/Ubicacion/Canton')[0].text
    if len(CountyNode) != 2 or CountyNode.isnumeric() == False:
        return "El nodo de Canton del Receptor no posee la estructura correcta. Solo debe contener dos dígitos y" \
               " debe ser un número. (Dato recibido: '" + str(CountyNode) + "', número de dígitos: " + str(len(CountyNode)) + ")"
    else:
        return True


def validateReceiverCity(data: xml.etree.ElementTree.Element):  # Distrito
    CityNode = data.findall('.//Receptor/Ubicacion/Distrito')[0].text
    if len(CityNode) != 2 or CityNode.isnumeric() == False:
        return "El nodo de Distrito del Receptor no posee la estructura correcta. Solo debe contener dos dígitos y" \
               " debe ser un número. (Dato recibido: '" + str(CityNode) + "', número de dígitos: " + str(len(CityNode)) + ")"
    else:
        return True


def validateReceiverNeighborhood(data: xml.etree.ElementTree.Element):  # Barrio
    try:
        NeighborhoodNode = data.findall('.//Receptor/Ubicacion/Barrio')[0].text
        if len(NeighborhoodNode) != 2 or NeighborhoodNode.isnumeric() == False:
            return "El nodo de Barrio del Receptor no posee la estructura correcta. Solo debe contener dos dígitos y" \
                   " debe ser un número. (Dato recibido: '" + str(NeighborhoodNode) + "', número de dígitos: " + str(len(NeighborhoodNode)) + ")"
        else:
            return True
    except:
        return True


def validateReceiverOtherSigns(data: xml.etree.ElementTree.Element):
    OtherSigns = data.findall('.//Receptor/Ubicacion/OtrasSenas')
    if len(OtherSigns) == 0:
        return "No existe Nodo de Ubicacion en XML"
    else:
        if len(OtherSigns[0].text) > 250:
            return "Excedido límite de caractreres para nodo OtrasSenas de Receptor. (Permitido: 250. Recibido: " + str(
                len(OtherSigns[0].text)) + ")"
        else:
            return True


def validateReceiverTelephone(data: xml.etree.ElementTree.Element):  # ***
    try:
        data.findall('.//Receptor/Telefono')
        telephoneResults = [validateReceiverTelephoneCountryCode(data), validateReceiverTelephoneNumber(data)]
        return telephoneResults
    except:
        return True


def validateReceiverTelephoneCountryCode(data: xml.etree.ElementTree.Element):
    CountryCode = data.findall('.//Receptor/Telefono/CodigoPais')[0].text
    if re.match(REOnlyNumbers, CountryCode) == False or len(CountryCode) != 3:
        return "Formato de código páis de número de teléfono de Receptor no es válido. Solo se permite un máximo de" \
               " 3 Números. (Recibido: " + CountryCode + ")."
    else:
        return True


def validateReceiverTelephoneNumber(data: xml.etree.ElementTree.Element):
    telephoneNumber = data.findall('.//Receptor/Telefono/NumTelefono')[0].text
    if re.match(REOnlyNumbers, telephoneNumber) == False or len(telephoneNumber) > 20:
        return "Formato de número telefónico de Receptor no es válido. Solo se permite un máximo de 20 números." \
               " (Recibido: " + str(telephoneNumber) + ")."
    else:
        return True


def validateReceiverFax(data: xml.etree.ElementTree.Element):  # ***
    try:
        data.findall('.//Receptor/Fax')
        faxResults = [validateReceiverTelephoneCountryCode(data), validateReceiverTelephoneNumber(data)]
        return faxResults
    except:
        return True


def validateReceiverFaxCountryCode(data: xml.etree.ElementTree.Element):
    CountryCode = data.findall('.//Receptor/Fax/CodigoPais')[0].text
    if re.match(REOnlyNumbers, CountryCode) == False or len(CountryCode) != 3:
        return "Formato de código páis de número de teléfono de Receptor no es válido. Solo se permite un máximo de" \
               " 3 Números. (Recibido: " + CountryCode + ")."
    else:
        return True


def validateReceiverFaxNumber(data: xml.etree.ElementTree.Element):
    FaxNumber = data.findall('.//Receptor/Fax/NumTelefono')[0].text
    if re.match(REOnlyNumbers, FaxNumber) == False or len(FaxNumber) > 20:
        return "Formato de número telefónico de Receptor no es válido. Solo se permite un máximo de 20 números." \
               " (Recibido: " + str(FaxNumber) + ")."
    else:
        return True


def validateReceiverEmail(data: xml.etree.ElementTree.Element):
    EmailNode = data.findall('.//Receptor/CorreoElectronico')
    if len(EmailNode) == 0:
        return "No se encuenta nodo de Correo Electronico de Receptor, el cual es de caracter olbigatorio."
    else:
        return True


def validateReceiverEmailDetail(data: xml.etree.ElementTree.Element):
    EmailNode = data.findall('.//Receptor/CorreoElectronico')[0].text
    if re.match(REEmailReceiver, EmailNode) == None or len(EmailNode) > 160:
        return "Formato de Correo Electronico de Receptor no es válido. (Recibido: " + EmailNode + ")"
    else:
        return True

# def validateSubNodes(root,ParentNodeName):
#    ParentNodePath = './/' + ParentNodeName +  '/*'
#    childTags = [t.tag for t in root.findall(ParentNodePath)]
#    for childNode in childTags:
#        print("ChildNode: " + childNode)
