# features/favoritos.txt - Operações com Favoritos

import json
import os

FAVORITOS_PATH = "data/favoritos.json"

def salvar_favorito(item_id, nome, qualidade, cidade):
    favorito = {"id": item_id, "nome": nome, "qualidade": qualidade, "cidade": cidade}
    favoritos = []
    if os.path.exists(FAVORITOS_PATH):
        with open(FAVORITOS_PATH, 'r', encoding='utf-8') as f:
            try:
                favoritos = json.load(f)
            except:
                favoritos = []
    if favorito not in favoritos:
        favoritos.append(favorito)
        with open(FAVORITOS_PATH, 'w', encoding='utf-8') as f:
            json.dump(favoritos, f, indent=4)

def carregar_favoritos():
    if os.path.exists(FAVORITOS_PATH):
        with open(FAVORITOS_PATH, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except:
                return []
    return []