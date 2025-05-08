# features/transporte.py - Simulador de Rota de Transporte

ROTAS = {
    ("Caerleon", "Martlock"): 0.8,
    ("Caerleon", "Bridgewatch"): 0.9,
    ("Caerleon", "Fort Sterling"): 1.0,
    ("Caerleon", "Lymhurst"): 0.7,
    ("Caerleon", "Thetford"): 1.2,
    ("Martlock", "Caerleon"): 0.8,
    ("Bridgewatch", "Caerleon"): 0.9,
    ("Fort Sterling", "Caerleon"): 1.0,
    ("Lymhurst", "Caerleon"): 0.7,
    ("Thetford", "Caerleon"): 1.2
}

def simular_custo_transporte(origem, destino, peso_total):
    try:
        taxa_por_kg = ROTAS.get((origem, destino), 1.5)
        custo_total = peso_total * taxa_por_kg
        return round(custo_total, 2)
    except Exception as e:
        return f"Erro: {str(e)}"

def obter_rotas_disponiveis():
    return list(set(ROTAS.keys()))