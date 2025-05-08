import requests
import json

url = "https://raw.githubusercontent.com/broderickhyman/ao-bin-dumps/master/items.json"
res = requests.get(url)

if res.status_code == 200:
    with open("config/itens_raw_api.json", "w", encoding="utf-8") as f:
        json.dump(res.json(), f, indent=4)
    print("✅ Arquivo salvo com sucesso!")
else:
    print("❌ Erro ao acessar a API:", res.status_code)
