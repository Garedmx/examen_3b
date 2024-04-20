# Proyecto Examen_3B

Este proyecto es una aplicación web desarrollada con FastAPI que realiza web scraping a la página https://iau.org/public/themes/naming_stars/ para obtener una lista de algunas estrellas y sus caracteristicas y proporcionarla a través de un endpoint. 

También incluye funcionalidades para guardar esta lista en un archivo JSON, para realizar actualizaciones en un archivo JSON existente mediante un endpoint POST y para guardar los archivos JSON individuales en un Contenedor de Azure Blob Storage.

## Requisitos

- Docker
- Python 3.x
- pip

## Instalación y Uso

1. Clona este repositorio en tu máquina local o Descomprimir el archivo .ZIP:
2. Navega al Directorio Raiz:
4. Ejecuta docker-compose para incializar los contenedores docker con: ´docker-compose up´
5. Accede a la aplicacion en tu navegador web: http://localhost:8000/

## Endpoints

- GET `/stars`: Devuelve una lista de todas las estrellas.

- GET `/stars?max=NUMERO_DE_REGISTROS`: Devuelve una lista limitada al ´max´ numero de registros que desees.

- POST `/star_mod`: Permite actualizar los atributos de un Pokémon existente o agregar uno nuevo.

- GET `/star_upload`: Almacena de manera individual en formato JSON dentro de un Contenedor la informacion de las estrellas consultadas.

## Variables de Entorno

Asegúrate de configurar las siguientes variables de entorno en un archivo `.env` en el directorio raíz del proyecto:

- `STORAGE_NAME`: Nombre del contenedor en Azure Blob Storage.

## Ejecutar Pruebas

Para hacer uso del sistema puede usar herramientas que le permitan consumir API's como postman o Thunder Client, en caso de no contar con alguno de ellos, el sistema cuenta con su propia interface de consulta de API en la ruta: http://localhost:8000/docs#

## Sección 4

Dentro de esta sección se explicaran los puntos solicitados en el ejercicio de prueba técnica.
### Herramientas y Tecnologías
Para el sistema en general decidí usar un patron de desarrollo basado en API's, así como el uso de contenedores en Docker y su configuracion en Docker-compose para un deploy mas automatizado, con esto se tiene la intención de demostrar el conocimiento del manejo de microservicios.

Tambien decido usar un versionador de codigo con el objetivo de mantener a lo mas pisible las best practices el cual es git, conectandolo con su herramienta de github para su futuro consumo.

Para el control de las API's se usa Fastapi como libreria de python ya que es la menos pesada y brinda todo lo necesario para el requerimiento de esta prueba.

Para el proceso de scraping se usa la libreria de BeautifulSoup para poder "parsear" el contenido html de la página objetivo, extrallendo una sabana de información y guardandola en un archivo local segun los requerimientos.

Para el facil manejo de la infromación, se decide usar las estructuras JSON, ya que se adecuan correctamente con el tipo de información obtenida de la página objetivo.

Por ultimo decido usar una conección al Cloud de Azure y usar su servicio de Azure Blob Storage para el almasenamiento de la información, esto con la clara intención de demostrar la versatilidad de conectividad con cualquiera de los hambientes Cloud lider en el mercado.
### Costos
Este requerimiento consume muy poco recurso ya que la infromación recabada se procesa como texto plano, siendo las consultas al storage lo mas costoso, en caso de requerir disminuir el costo, se puede recomendar cambiar la logica de almacenamiento y en ligar de almacenar por estrella, podemos almacenar por consulta de estrellas, reduciendo la peticion en el servicio de storage.
### Rendimiento
El proyecto ya se encuentra optimizado para poder ser montado en una pipeline de CI//CD, sin hembargo se puede mejorar si se implementara kubernets para la gestion de los hambientes de deploy en los servicios cloud, tambien se puede optimizar el tiempo de storage con un Bucket de almacenamiento mas robusto

## Autor

Edgar Francisco Santana Muirillo
