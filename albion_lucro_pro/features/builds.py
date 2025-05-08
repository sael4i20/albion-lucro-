# features/builds.py - Gerenciamento de Builds

import os
import json

BUILDS_PATH = "data/builds"

def montar_build_simples(build_dict):
    resultado = []
    for posicao, item in build_dict.items():
        nome = item.get("nome", "").capitalize()
        tier = item.get("tier", "")
        enc = item.get("enc", "")
        resultado.append(f"{posicao}: {tier} {nome}{enc}")
    return "\n".join(resultado)

def salvar_build(nome, build_dict):
    if not os.path.exists(BUILDS_PATH):
        os.makedirs(BUILDS_PATH)
    path = f"{BUILDS_PATH}/{nome}.json"
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(build_dict, f, indent=4)

def carregar_builds_disponiveis():
    if not os.path.exists(BUILDS_PATH):
        return []
    return [f.replace(".json", "") for f in os.listdir(BUILDS_PATH) if f.endswith(".json")]

def carregar_build(nome):
    path = f"{BUILDS_PATH}/{nome}.json"
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)