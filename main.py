from fastapi import FastAPI
from app.scraper import Scrape
import json

app = FastAPI()

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
