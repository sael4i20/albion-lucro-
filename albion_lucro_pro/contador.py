import json

with open("config/itens_raw_api.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

# Se os dados forem uma lista de objetos
if isinstance(dados, list):
    ids = [item.get("UniqueName") for item in dados if "UniqueName" in item]
    ids = [i for i in ids if i and "/" not in i]  # ignora compostos
    print(f"Total de itens válidos: {len(ids)}")
    print("Exemplo de IDs:", ids[:10])
else:
    print("⚠️ O arquivo não está no formato de lista como esperado.")
