from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

import requests

# Define la URL base del servidor FastAPI
BASE_URL = "http://localhost:8000"

# Prueba GET /stars
def test_get_stars():
    response = requests.get(f"{BASE_URL}/stars?max=3")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    
# Prueba POST /star_mod
def test_post_star_mod():
    data = [  
        {
            "IAU_Name": "Alasia",
            "Vmag": "20.95"
        },
        {
            "IAU_Name": "Amansinaya",
            "Designation": "WASP-34",
            "ID": "_",
            "Const": "Crt",
            "No": "_",
            "WDS_J": "_",
            "Vmag": "40.30",
            "RA": "165.399575",
            "Dec": "-23.860662",
            "Approval_Date": "2019-12-17"
        },
        {
            "IAU_Name": "SOL",
            "Designation": "Via Lactea",
            "ID": "_",
            "Const": "Crt",
            "No": "_",
            "WDS_J": "_",
            "Vmag": "40.30",
            "RA": "165.399575",
            "Dec": "-23.860662",
            "Approval_Date": "0000-00-00"
        }      
    ]
    response = requests.post(f"{BASE_URL}/star_mod", json=data)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
