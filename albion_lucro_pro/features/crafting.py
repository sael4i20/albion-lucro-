# features/crafting.txt - Lógica de simulação de Crafting e Refino

def calcular_custo_crafting(quantidade, taxa, retorno):
    try:
        custo_base = quantidade * 1000  # valor estimado de custo por item (ajustável)
        custo_taxado = custo_base * (1 + taxa)
        recuperado = custo_base * retorno
        custo_final = custo_taxado - recuperado
        return int(custo_final)
    except Exception as e:
        return f"Erro: {str(e)}"