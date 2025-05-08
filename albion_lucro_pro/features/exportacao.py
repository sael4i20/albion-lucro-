# features/exportacao.txt - Exportação de resultados para CSV

import csv
import os
from datetime import datetime

EXPORT_PATH = "export"

def exportar_resultados_csv(nome_base, dados, colunas):
    if not os.path.exists(EXPORT_PATH):
        os.makedirs(EXPORT_PATH)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"{nome_base}_{timestamp}.csv"
    caminho = os.path.join(EXPORT_PATH, nome_arquivo)

    try:
        with open(caminho, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=colunas)
            writer.writeheader()
            for linha in dados:
                writer.writerow(linha)
        return caminho
    except Exception as e:
        return f"Erro ao exportar: {e}"