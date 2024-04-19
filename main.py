from fastapi import FastAPI
from app.scraper import scrape_stars_list

app = FastAPI()

@app.get("/")
async def index():
    return {"message": "Hola mundo"}

@app.get("/stars")
async def get_stars():
    stars_list = scrape_stars_list()
    return {"stars": stars_list}
