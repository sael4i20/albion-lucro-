# utils/auto_fix.txt - Diagnóstico e Correção Automática

import os
import json

class AutoFixer:
    def __init__(self):
        self.pastas_criticas = [
            "assets", "assets/icones", "assets/fundo", "audio", "audio/cliques",
            "audio/musica_fundo", "data", "data/crafting", "data/builds", "config", "logs"
        ]
        self.arquivos_padrao = {
            "config/settings.json": {},
            "data/favoritos.json": [],
            "logs/erros.log": ""
        }

    def diagnostico_geral(self):
        problemas = []
        for pasta in self.pastas_criticas:
            if not os.path.exists(pasta):
                os.makedirs(pasta)
                problemas.append(f"[Criado] Pasta ausente: {pasta}")
        for arquivo, conteudo in self.arquivos_padrao.items():
            if not os.path.exists(arquivo):
                with open(arquivo, 'w', encoding='utf-8') as f:
                    if isinstance(conteudo, dict):
                        json.dump(conteudo, f, indent=4)
                    elif isinstance(conteudo, list):
                        json.dump(conteudo, f)
                    else:
                        f.write(str(conteudo))
                problemas.append(f"[Criado] Arquivo ausente: {arquivo}")
        if not problemas:
            return "[AutoFixer] Tudo verificado. Nenhum problema encontrado."
        else:
            return "\n".join(problemas)