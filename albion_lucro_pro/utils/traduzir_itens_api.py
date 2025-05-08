import json

RAW_PATH = "config/itens_raw_api.json"
DESTINO_PATH = "config/itens_traduzidos.json"

def traduzir_itens():
    with open(RAW_PATH, "r", encoding="utf-8") as f:
        dados = json.load(f)

    traduzidos = {}

    for item in dados:
        if not isinstance(item, dict):  # <-- ignora se for string ou outro tipo
            continue

        if item.get("Marketable") and isinstance(item.get("LocalizedNames"), dict):
            nome_br = item["LocalizedNames"].get("PT-BR")
            if nome_br:
                traduzidos[nome_br.lower()] = item.get("UniqueName", "")

    if traduzidos:
        with open(DESTINO_PATH, "w", encoding="utf-8") as f_out:
            json.dump(traduzidos, f_out, ensure_ascii=False, indent=2)
        print(f"✅ {len(traduzidos)} itens traduzidos salvos em: {DESTINO_PATH}")
    else:
        print("⚠️ Nenhum item com nome PT-BR encontrado.")

if __name__ == "__main__":
    traduzir_itens()
