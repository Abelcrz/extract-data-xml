import xml.etree.ElementTree as ET
import csv
import os
import glob

# Función para parsear un solo archivo XML
def parse_xml(file_path):
    print(file_path)
    tree = ET.parse(file_path)  # Cargar el XML desde la ruta
    root = tree.getroot()  # Obtener el nodo raíz
    return root

# Función para extraer los datos de cada archivo XML
def extract_data_from_xml(root,tipo_doc):
        data = []
        tipo=tipo_doc
        # Obtener el nodo 'Comprobante'
        comprobante_atributos = root.attrib
        # Mostrar los atributos
        for key, value in comprobante_atributos.items():
            #print(f"{key}: {value}")
            if key == "Version":
                version_comprobante = value
            if key == "Serie":
                serie_comprobante = value                   
            if key == "Folio":
                folio_comprobante = value       
            if key == "Fecha":
                fecha_comprobante = value                               
            if key == "LugarExpedicion":
                lugar_comprobante = value    
            if key == "Moneda":
                moneda_comprobante = value   
            if key == "TipoCambio":
                tipocambio_comprobante = value                   
            if key == "SubTotal":
                subtotal_comprobante = value                       
            if key == "Total":
                total_comprobante = value                                  
            if key == "TipoDeComprobante":
                tipo_comprobante = value           
            if key == "FormaPago":
                formapago_comprobante = value      
            if key == "MetodoPago":
                metodopago_comprobante = value                    
            if key == "CondicionesDePago":
                condicionpago_comprobante = value      

       # Buscar el nodo <Emisor>
        emisor = root.find('.//Emisor')
        if emisor is None:
            emisor = root.find('.//cfdi:Emisor', namespaces={'cfdi': 'http://www.sat.gob.mx/cfd/3'})
        if emisor is not None:
            nombre_emisor = emisor.get('Nombre')
            rfc_emisor = emisor.get('Rfc')
        else:
            print("No se encontró el Emisor")

        # Buscar el nodo <Receptor>
        receptor = root.find('.//Receptor')
        if receptor is None:
            receptor = root.find('.//cfdi:Receptor', namespaces={'cfdi': 'http://www.sat.gob.mx/cfd/3'})
        if receptor is not None:
            nombre_receptor = receptor.get('Nombre')
            rfc_receptor = receptor.get('Rfc')
            print(f"Receptor: {nombre_receptor}, Rfc: {rfc_receptor}")
        else:
            print("No se encontró el Receptor")




        # Buscar el nodo <Receptor>
        # Buscar el atributo TotalImpuestosTrasladados
        # Buscar todos los nodos <Traslado> y extraer el atributo Importe
        impuesto_traslados =""
        traslados = root.find("Impuestos//Traslados//Traslado" )
        #total_impuestos = root.find('.//cfdi:Impuestos', namespaces={'cfdi': 'http://www.sat.gob.mx/cfd/3'})

        #total_impuestos_trasladados = root.find('.//Impuestos').attrib['TotalImpuestosTrasladados']
        if traslados is None:
            traslados = root.find("cfdi:Impuestos//cfdi:Traslados//cfdi:Traslado"  , namespaces={'cfdi': 'http://www.sat.gob.mx/cfd/3'})

        # Extraer el atributo Importe de cada Traslado
        if traslados is not None:
            traslados_atributos = traslados.attrib
            for key, value  in traslados_atributos.items():
                if key == "Importe":
                    impuesto_traslados = value        

        # Buscar el nodo 'TimbreFiscalDigital'
        # Buscar el UUID dentro de TimbreFiscalDigital
        uui_fiscal = ""
        fechatimbrado_fiscal = ""
        timfis = root.find('.//Complemento//TimbreFiscalDigital' )
        if timfis is None:
            namespaces = {
                'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital'
            }
            timfis = root.find('.//tfd:TimbreFiscalDigital'  , namespaces=namespaces )
    
        if timfis is not None:
            timbre_fiscal_atributos = timfis.attrib
            for key, value  in timbre_fiscal_atributos.items():
                if key == "UUID":
                    uui_fiscal = value
                if key == "FechaTimbrado":
                    fechatimbrado_fiscal = value                    
 
        data.append([tipo,nombre_emisor, rfc_emisor, nombre_receptor, rfc_receptor, uui_fiscal ,version_comprobante, serie_comprobante ,folio_comprobante, fecha_comprobante, lugar_comprobante, moneda_comprobante,tipocambio_comprobante,subtotal_comprobante, 0,0,impuesto_traslados ,total_comprobante, tipo_comprobante, formapago_comprobante, metodopago_comprobante, condicionpago_comprobante, fechatimbrado_fiscal ])  # Guardar en una lista
        return data

# Función para guardar los datos extraídos en un archivo CSV
def save_to_csv(data, output_csv_path):
    with open(output_csv_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:  # Si el archivo está vacío
            writer.writerow(['Tipo','Emisor', 'Emisor RFC','Receptor','Receptor RFC','Folio fiscal','Version','Serie','Folio','Fecha','Lugar','Moneda','Tipo de Cambio','Subtotal','Descuento','Impuestos Retenidos','Impuestos Trasladados','Total','Tipo Comprobante','Forma de Pago','Método de Pago','Condiciones de Pago','Fecha Timbrado'])  # Escribe las cabeceras

        writer.writerows(data)  # Escribir los datos extraídos

# Función para procesar múltiples archivos XML y guardarlos en un CSV
def process_multiple_xml_to_csv(xml_files, output_csv_path,tipo):
    all_data = []  # Lista que acumula todos los datos de los XML
    for xml_file in xml_files:
        if os.path.exists(xml_file):  # Verificar si el archivo XML existe
            root = parse_xml(xml_file)  # Parsear el XML
            data = extract_data_from_xml(root, tipo)  # Extraer los datos
            all_data.extend(data)  # Agregar los datos extraídos a la lista total
            root = ""

        else:
            print(f"El archivo {xml_file} no existe.")  # Mensaje de error si el archivo no se encuentra
    save_to_csv(all_data, output_csv_path)  # Guardar todos los datos en un CSV


# Función para obtener los archivos XML en un directorio

##def get_xml_files(directory_path):
    ##return glob.glob(os.path.join(directory_path, '*.xml'))

# Ejemplo de uso

##directory = 'CONTABILIDAD_FACTURAS'  # Ruta donde están los archivos XML
##xml_files2 = get_xml_files(directory)
##print(xml_files2)

def save_URL_csv(data, output_csv_path):
    with open(output_csv_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:  # Si el archivo está vacío
            writer.writerow(['URLs'])  # Escribe las cabeceras
        for archivo in data:
            writer.writerow([archivo])  # Escribe cada archivo en una nueva fila



def buscar_archivos(directorio, anioMes, sucursal, tipo, extension=None):
    # Recorre todas las carpetas y subcarpetas
    dataURL= []
    for raiz, dirs, archivos in os.walk(directorio +"/"+ anioMes):
        for archivo in archivos:
            # Si se especifica una extensión, filtra los archivos con esa extensión
            if extension is None or archivo.endswith(extension):
                #print(f'Archivo encontrado: {os.path.join(raiz, archivo)}')
                dataURL.append(os.path.join(raiz, archivo))
                #save_to_csv(f'Archivo encontrado: {os.path.join(raiz, archivo)}', "CONTABILIDAD_FACTURAS/archivo_salida_rutas.csv")  # Guardar todos los datos en un CSV
                
    #print(dataURL)
    save_URL_csv(dataURL,directorio +"/"+ anioMes + "/urls" + anioMes + ".csv")
    csv_file = directorio +"/"+ anioMes + "/"+ anioMes +" - "+ tipo +" "+ sucursal +".csv"  # Ruta donde guardar el archivo CSV
    process_multiple_xml_to_csv(dataURL, csv_file, tipo)
# Ejemplo de uso: buscar archivos .txt en una carpeta y subcarpetas

sucursal_sr = "San Rafael"
directorio_sr = '//ve-bfc03/Doctos_Respaldo/Facts/2019'  

sucursal_mx = "Mexico"
directorio_mx = '//dapesa07/facts/2019'  

sucursal_my = "Monterrey"
directorio_my = '//mty-dc01/Doctos/Facts/2019'  

sucursal_ln = "Leon"
directorio_ln = '//gto-nas01/Doctos/facts/2019'  

dir_anio_mes = '2019-01'  # Cambia esto a la ruta de tu carpeta

tipo_doc = "Factura"
buscar_archivos(directorio_my, dir_anio_mes, sucursal_my, tipo_doc, '.xml')  # Si quieres buscar por tipo de archivo



def extraer_emisor(ruta_xml):
    try:
        # Parsear el archivo XML
        tree = ET.parse(ruta_xml)
        root = tree.getroot()

        # Buscar el emisor usando el nombre de la etiqueta
        emisor = root.find('.//Receptor')
        emisor = root.find('.//Receptor')
        if emisor is None:
            # Encontrar el emisor
            emisor = root.find('.//cfdi:Receptor', namespaces={'cfdi': 'http://www.sat.gob.mx/cfd/3'})

        if emisor is not None:
            nombre_emisor = emisor.get('Nombre')
            rfc_emisor = emisor.get('Rfc')
            regimen_fiscal = emisor.get('RegimenFiscal')

            # Mostrar los resultados
            print(f'Emisor encontrado en {ruta_xml}:')
            print(f'  Nombre: {nombre_emisor}')
            print(f'  RFC: {rfc_emisor}')
            print(f'  Régimen Fiscal: {regimen_fiscal}')
            print('-' * 50)
        else:
            print(f'No se encontró el emisor en {ruta_xml}.')
            print('-' * 50)
    except Exception as e:
        print(f'Error al procesar el archivo {ruta_xml}: {e}')
        print('-' * 50)


# Iterar sobre cada ruta y procesar el archivo
##for ruta in xml_files2:
##    extraer_emisor(ruta)
# Recorrer cada archivo en el array xml_files
#for xml_f in xml_files2:
#    print(f'Procesando el archivo: {xml_f}')
#    csv_file = 'C:/Users/abel.cruz/Documents/CONTABILIDAD_FACTURAS/archivo_salida.csv'  # Ruta donde guardar el archivo CSV
    #process_multiple_xml_to_csv(xml_f, csv_file)
    # Aquí puedes agregar el código para procesar cada archivo
    # Por ejemplo, podrías llamara una función como process_xml_to_csv(xml_file)
    # process_xml_to_csv(xml_file)