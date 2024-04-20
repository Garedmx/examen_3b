from fastapi import FastAPI, Query, HTTPException
from app.scraper import Scrape
from pydantic import BaseModel
from typing import Optional, List
import json

app = FastAPI()

class StarData(BaseModel):
    IAU_Name: str
    Designation:Optional[str]
    ID: Optional[str]
    Const: Optional[str]
    No: Optional[str]
    WDS_J: Optional[str]
    Vmag: Optional[str]
    RA: Optional[str]
    Dec: Optional[str]
    Approval_Date: Optional[str]
 

@app.get("/")
def index():
    steps= {
        "Paso 1": "Para iniciar el Scraping ingrese a la URL http://127.0.0.1:8000/stars?max=10",
        "Paso 2": "Para modificar un dato, proporcione una consulta POST a la URL http://127.0.0.1:8000/star_mod y en formanto JSON los datos a Modificar",
        "Paso 3": "Para almacenar la informacion en Azure Blob Storage ingrese a la URL http://127.0.0.1:8000/star_upload"
    }
        
    return {f"Hola Mundo": "Este es un sistema desarrollado como ejercicio para 3B por el puesto de Backend Developer", "Instrucciones": steps}


@app.get("/stars", response_model=dict)
def get_stars(max: int = Query(None, description="Número máximo de estrellas a consultar")):
    new_scrape = Scrape()
    stars_list = new_scrape.scrape_stars_list(max=max)
    if stars_list["status"] == "success":
        new_scrape.scrape_stars_local_save()
        return {"status": "success", "data": json.loads(stars_list["data"])}
    else:
        return {"status": "error", "message": stars_list["message"]}


@app.post("/star_mod")
def update_star_data(star_data_list: List[StarData]):
    # Convertir el objeto Pydantic a una lista de diccionarios
    star_data_dicts = [star_data.dict() for star_data in star_data_list]
    new_scrape = Scrape()
    stars_list = new_scrape.scrape_modif_data(star_data_dicts)

    if stars_list["status"] == "success":
        return {"status": "success", "message": stars_list["message"], "data": json.loads(stars_list["data"])}
    else:
        return {"status": "error", "message": stars_list["message"]}


@app.get("/star_upload")
def upload_star_data():
    new_scrape = Scrape()
    stars_list = new_scrape.scrape_stars_upload()

    if stars_list["status"] == "success":
        return {"status": "success", "message": stars_list["message"], "data": json.loads(stars_list["data"])}
    else:
        return {"status": "error", "message": stars_list["message"]}