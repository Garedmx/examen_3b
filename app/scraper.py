from bs4 import BeautifulSoup
from datetime import datetime
import requests
import json
import os

class Scrape:
    def __init__(self):
        self.url = 'https://iau.org/public/themes/naming_stars/'
        self.json_data = []

    def scrape_stars_list(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            stars_list = []
            table = soup.find('table', class_='table table-striped sortable')
            if table:
                columns = [column.text.strip() for column in table.find('tr').find_all('th')]
                for row in table.find_all('tr')[1:]:
                    cells = row.find_all('td')
                    star_info = {}
                    for index, cell in enumerate(cells):
                        star_info[columns[index]] = cell.text.strip()
                    stars_list.append(star_info)
                self.json_data = json.dumps(stars_list, indent=2)
                return {"status": "success", "data": self.json_data}
            else:
                return {"status": "error", "message": "No se encontró la tabla en la página."}
        else:
            return {"status": "error", "message": f"No se pudo acceder a la página. Código de estado: {response.status_code}"}
        
        
    def scrape_stars_local_save(self):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"data_{timestamp}.json"
        folder_path = "data"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_path = os.path.join(folder_path, filename)
        data = json.loads(self.json_data)
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
