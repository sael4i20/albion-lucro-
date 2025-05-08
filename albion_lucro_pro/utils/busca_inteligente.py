import json
import os
from difflib import get_close_matches

ARQUIVO_ITENS = "config/itens_raw_api.json"
RAW_JSON_PATH = "config/itens_raw_api.json"

def buscar_item_id(nome_digitado):
    nomes_disponiveis = list(BASE_ITENS.keys())

    if isinstance(nome_digitado, list):
        if not nome_digitado:
            return None, None
        nome_digitado = nome_digitado[0]

    nome_digitado = nome_digitado.lower()
    correspondencias = get_close_matches(nome_digitado, nomes_disponiveis, n=1, cutoff=0.6)

    if correspondencias:
        nome_mais_proximo = correspondencias[0]
        return BASE_ITENS[nome_mais_proximo], nome_mais_proximo

    return None, None


BASE_ITENS = carregar_base_itens()

def buscar_item_id(nome_digitado):
    nomes_disponiveis = list(BASE_ITENS.keys())

    if isinstance(nome_digitado, list):
        if not nome_digitado:
            return None
        nome_digitado = nome_digitado[0]

    correspondencias = get_close_matches(str(nome_digitado).lower(), nomes_disponiveis, n=1, cutoff=0.6)

    if correspondencias:
        nome_mais_proximo = correspondencias[0]
        return BASE_ITENS[nome_mais_proximo], nome_mais_proximo

    return None, None

def buscar_item_semelhante(parcial):
    return [nome for nome in BASE_ITENS if parcial.lower() in nome.lower()]
