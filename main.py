from fastapi import FastAPI, HTTPException
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
        "Paso 1": "Para iniciar el Scraping ingrese a la URL http://127.0.0.1:8000/stars",
        "Paso 2": "Para modificar un dato, proporcione una consulta POST a la URL http://127.0.0.1:8000/star_mod/<IAU Name> y en formanto JSON los datos a Modificar",
        "Paso 3": "Para almacenar la informacion en Azure Blob Storage ingrese a la URL http://127.0.0.1:8000/stars_save"
    }
        
    return {f"Hola Mundo": "Este es un sistema desarrollado como ejercicio para 3B por el puesto de Backend Developer", "Instrucciones": steps}


@app.get("/stars", response_model=dict)
def get_stars():
    new_scrape = Scrape()
    stars_list = new_scrape.scrape_stars_list()
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

    #return stars_list

    if stars_list["status"] == "success":
        return {"status": "success", "message": stars_list["message"], "data": json.loads(stars_list["data"])}
    else:
        return {"status": "error", "message": stars_list["message"]}

    