from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient, PublicAccess, AccessPolicy, ContainerSasPermissions
import requests
import json
import os


class Scrape:
    def __init__(self):
        self.url = 'https://iau.org/public/themes/naming_stars/'
        self.json_data = []

    def scrape_stars_list(self, max):
        response = requests.get(self.url)

        # Validamos una respuesta success
        if response.status_code == 200:

            # Se realiza el Parseo del contenido HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            stars_list = []

            # Se encuentra la tabla de contenido
            table = soup.find('table', class_='table table-striped sortable')

            # Se valida la existencia de la tabla
            if table:
                # Obtener los títulos de las columnas (primera fila de la tabla)
                columns = [column.text.strip() for column in table.find('tr').find_all('th')]

                # Aplicar transformaciones a los títulos de las columnas
                transformed_columns = []
                for column in columns:
                    # Sustituir los espacios por '_'
                    column = column.replace(' ', '_')
                    # Sustituir los puntps por ''
                    column = column.replace('.', '')
                    # Sustituir '#' por 'No'
                    column = column.replace('#', 'No')
                    # Eliminar los paréntesis y su contenido
                    column = column.split('(')[0].strip()
                    transformed_columns.append(column)

                # Iterar sobre las filas de la tabla (excepto la primera que contiene los títulos de las columnas)
                for row in table.find_all('tr')[1:max +1]:
                    # Obtener las celdas de la fila
                    cells = row.find_all('td')
                    # Crear un diccionario para almacenar la información de la fila
                    star_info = {}
                    # Iterar sobre las celdas y asignar el contenido al diccionario utilizando los títulos de las columnas como claves
                    for index, cell in enumerate(cells):
                        star_info[transformed_columns[index]] = cell.text.strip()

                    # Agregar el diccionario a la lista de estrellas    
                    stars_list.append(star_info)
                # Convertir la lista de estrellas a formato JSON    
                self.json_data = json.dumps(stars_list, indent=2)

                return {"status": "success", "data": self.json_data}
            else:
                return {"status": "error", "message": "No se encontró la tabla en la página."}
        else:
            return {"status": "error", "message": f"No se pudo acceder a la página. Código de estado: {response.status_code}"}
        
        
    def scrape_stars_local_save(self):
        # Obtener la fecha y hora actual como un timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Nombre del archivo JSON con el timestamp de ejecución
        filename = f"data_{timestamp}.json"

        # Carpeta donde se guardarán los archivos JSON
        folder_path = "data"

        # Verificar si la carpeta existe, si no, crearla
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Ruta completa del archivo JSON  
        file_path = os.path.join(folder_path, filename)

        # Codificamos en formato Json
        data = json.loads(self.json_data)

        # Escribir el contenido en el archivo JSON
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)


    def scrape_modif_data(self, star_data_dicts):
        # Obtener la lista de archivos en la carpeta "datos"
        folder_path = "data"
        file_list = os.listdir(folder_path)

        star_data_json = json.dumps(star_data_dicts)
        

        # Ordenar los archivos por fecha de modificación (el último archivo será el último de la lista)
        file_list.sort(key=lambda x: os.path.getmtime(os.path.join(folder_path, x)), reverse=True)

        # Obtener la ruta del último archivo de la lista
        latest_file_path = os.path.join(folder_path, file_list[0])

        # Leer el contenido del último archivo JSON
        with open(latest_file_path, "r") as json_file:
            stars_data = json.load(json_file)

        # Iterar sobre cada estrella en la lista de estrellas recibidas en la solicitud POST
        for star_data_dict in star_data_dicts:
            # Buscar si el registro ya existe en el archivo
            for star in stars_data:
                if star["IAU_Name"] == star_data_dict["IAU_Name"]:
                    # Actualizar los atributos del registro solo si el nuevo valor no es None
                    for key, value in star_data_dict.items():
                        if value is not None:
                            self.write_change_log(latest_file_path, star[key], value)
                            star[key] = value
                            
                    break
            else:
                # Si el registro no existe, agregarlo al final de la lista
                stars_data.append(star_data_dict)

        # Escribir los datos actualizados en el archivo JSON
        with open(latest_file_path, "w") as json_file:
            json.dump(stars_data, json_file, indent=4)

        return {"status": "success", "message": "Datos de estrella actualizados correctamente", "data": star_data_json}
    

    def write_change_log(self, file_path, old_data, new_data):
        log_file = "Log.txt"
        # Comprobar si el archivo de registro existe, si no, crearlo
        if not os.path.exists(log_file):
            with open(log_file, "w") as f:
                f.write("Nombre del Archivo  | Fecha de Cambio | Dato Anterior | Dato Nuevo\n")
        # Obtener la hora actual
        change_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Escribir el registro de cambio en el archivo de registro
        with open(log_file, "a") as f:
            f.write(f"{file_path} | {change_time} | {old_data} | {new_data}\n")

    def scrape_stars_upload(self):
        load_dotenv()
        star_data_dicts = {
            "storage_name" : os.getenv("STORAGE_NAME")
        }

        folder_path = "data"
        file_list = os.listdir(folder_path)

        # Ordenar los archivos por fecha de modificación (el último archivo será el último de la lista)
        file_list.sort(key=lambda x: os.path.getmtime(os.path.join(folder_path, x)), reverse=True)

        # Obtener la ruta del último archivo de la lista
        latest_file_path = os.path.join(folder_path, file_list[0])

        #limpiamos el nombre del contenedor
        container_name =  file_list[0].replace('_', '')
        container_name =  container_name.replace('/', '')
        container_name = container_name.split('.')[0].strip()


        # Obtenemos la cadena de coneccion a Azure del archivo .env
        connection_string = os.getenv("CADENA")

        # Conectamos con el servicio de Azure
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Verificamos la existencia del contenedor en caso contrario lo creamos dentro de Azure Blob Storage
        container_client = blob_service_client.get_container_client(container_name)
        if not container_client.exists():
            container_client.create_container()
            metadata = {'type': 'test'}
            container_client.set_container_metadata(metadata=metadata)
            access_policy = AccessPolicy(permission=ContainerSasPermissions(read=True), expiry=datetime.utcnow() + timedelta(days=7), start=datetime.utcnow() - timedelta(minutes=5))
            identifiers = {'test': access_policy}

            # Establecer el nivel de acceso público del contenedor como "blob"
            container_client.set_container_access_policy(signed_identifiers= identifiers, public_access=PublicAccess.CONTAINER)

        # Obtener la URL de acceso público del contenedor
        container_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}"

        star_data_dicts["container_name"] = container_name
        star_data_dicts["container_url"] = container_url

        #Abrimos el archivo JSON para cargarlo como variable
        with open(latest_file_path, "r") as json_file:
            stars_data = json.load(json_file)

        files_storage = []
        # Iteramos cada uno de los registros del ultimo archivo JSON
        for star in stars_data:
            blob_name = star["IAU_Name"]
            blob_name_file = blob_name + '.json'
            # Crear un nuevo archivo JSON para cada estrella
            with open(blob_name_file, "w") as blob_json_file:
                json.dump(star, blob_json_file)

            # Cargar el archivo JSON en Azure Blob Storage
            blob_client = container_client.get_blob_client(blob_name_file)
            files_storage.append(blob_name_file)
            with open(blob_name_file, "rb") as data:
                blob_client.upload_blob(data)
            # Eliminar el archivo JSON local después de cargarlo en Azure Blob Storage
            os.remove(blob_name_file)

        star_data_dicts["files"] = files_storage
        star_data_json = json.dumps(star_data_dicts)
        return {"status": "success", "message": "Datos cargados a Azure Blob Storage", "data": star_data_json}