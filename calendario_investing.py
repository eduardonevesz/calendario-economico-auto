import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import json
import csv

tz = pytz.timezone('America/Sao_Paulo')
data_hoje = datetime.now(tz).strftime("%Y-%m-%d")

url = "https://br.investing.com/economic-calendar/"
headers = {"User-Agent": "Mozilla/5.0"}
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.content, "html.parser")

eventos = []

for row in soup.select("tr.js-event-item"):
    try:
        data_evento = row["data-event-datetime"]
        if data_evento.startswith(data_hoje):
            hora = row.select_one("td.time").text.strip()
            moeda = row.select_one("td.flagCur span").text.strip()
            evento = row.select_one("td.event").text.strip()
            eventos.append({"hora": hora, "moeda": moeda, "evento": evento})
    except:
        continue

# Salvar como JSON
with open("eventos_hoje.json", "w", encoding="utf-8") as f:
    json.dump(eventos, f, ensure_ascii=False, indent=2)

# Salvar como CSV
with open("eventos_hoje.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["hora", "moeda", "evento"])
    writer.writeheader()
    writer.writerows(eventos)
