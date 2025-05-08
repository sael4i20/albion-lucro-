
import json
import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from time import sleep
import time

# Caminhos
RAW_JSON_PATH = "config/itens_raw_api.json"
OUTPUT_JSON = "config/itens_traduzidos_completo.json"
ICON_DIR = "assets/icones"

# Criar pasta de ícones, se necessário
os.makedirs(ICON_DIR, exist_ok=True)

# Cabeçalho para requisições
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Carrega lista de IDs dos itens
with open(RAW_JSON_PATH, "r", encoding="utf-8") as f:
    item_ids = json.load(f)

traduzidos = {}
falhas = []

for item in tqdm(item_ids, desc="⛏️ Extraindo nomes e ícones"):
    item_id = item.get("UniqueName", "").strip()
    if not item_id:
        continue

    url = f"https://albiononline2d.com/pt/item/{item_id}"
    try:
        res = requests.get(url, headers=headers, timeout=15)
        if res.status_code != 200:
            falhas.append((item_id, f"status {res.status_code}"))
            continue

        soup = BeautifulSoup(res.text, "html.parser")
        titulo = soup.find("h2")
        if not titulo:
            falhas.append((item_id, "sem título"))
            continue

        nome_br = titulo.text.strip()
        traduzidos[nome_br.lower()] = item_id

        # Baixar imagem
        img_tag = soup.find("img", {"alt": item_id})
        if img_tag and "src" in img_tag.attrs:
            img_url = "https://albiononline2d.com" + img_tag["src"]
            img_res = requests.get(img_url, stream=True)
            if img_res.status_code == 200:
                with open(f"{ICON_DIR}/{item_id}.png", "wb") as out:
                    for chunk in img_res.iter_content(chunk_size=8192):
                        out.write(chunk)

    except Exception as e:
        falhas.append((item_id, str(e)))

    sleep(30)  # Pausa de 30 segundos entre cada item

# Salva JSON traduzido
with open(OUTPUT_JSON, "w", encoding="utf-8") as f_out:
    json.dump(traduzidos, f_out, ensure_ascii=False, indent=2)

print(f"✅ {len(traduzidos)} itens traduzidos salvos em: {OUTPUT_JSON}")

# Log de falhas (opcional)
if falhas:
    print(f"⚠️ {len(falhas)} falhas durante a execução. IDs com erro foram:")
    for item, erro in falhas:
        print(f"  - {item}: {erro}")
