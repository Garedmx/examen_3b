from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def test():
    blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=storage3b;AccountKey=MDClPZnJ+R/kA1rDP+sPRRyppJCl09K9vTOWFNBc44gZ/givYzUolULX66u5xrVGQeJGtefrmfy++ASt59auuQ==;EndpointSuffix=core.windows.net")
    container_client = blob_service_client.get_container_client('prueba-edgarfranciscos')
    container_client.create_container()