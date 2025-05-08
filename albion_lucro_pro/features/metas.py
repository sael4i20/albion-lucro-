# features/metas.py - Sistema de Metas de Lucro

import json
import os
from datetime import datetime

METAS_PATH = "data/metas/meta_diaria.json"

def salvar_meta(valor):
    if not os.path.exists("data/metas"):
        os.makedirs("data/metas")
    meta = {
        "meta": valor,
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(METAS_PATH, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=4)

def carregar_meta():
    if os.path.exists(METAS_PATH):
        with open(METAS_PATH, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return {"meta": 0, "data": ""}
    return {"meta": 0, "data": ""}