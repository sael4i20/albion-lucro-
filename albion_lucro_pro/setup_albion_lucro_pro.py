# setup_albion_lucro_pro.py - Gera toda a estrutura do projeto automaticamente

import os

PASTAS = [
    "utils", "features", "assets", "assets/icones", "assets/fundo", "assets/scrollbar", "assets/botoes",
    "audio", "audio/cliques", "audio/musica_fundo", "data", "data/builds", "data/crafting", "data/metas",
    "data/transporte", "config", "logs", "export", "api_cache", "temp", "screenshots"
]

ARQUIVOS_VAZIOS = {
    "config/settings.json": "{}",
    "data/favoritos.json": "[]",
    "logs/erros.log": ""
}

def criar_pastas():
    for pasta in PASTAS:
        os.makedirs(pasta, exist_ok=True)

def criar_arquivos_vazios():
    for caminho, conteudo in ARQUIVOS_VAZIOS.items():
        with open(caminho, 'w', encoding='utf-8') as f:
            f.write(conteudo)

def mostrar_instrucoes():
    print("""\n
✅ Estrutura criada com sucesso!

Agora faça o seguinte:
1. Coloque seus arquivos de código nas pastas corretas:
    - 'main.py' na raiz
    - arquivos da pasta 'utils' e 'features' nos locais certos
2. Adicione sua imagem de fundo em 'assets/fundo/bg_app.png'
3. Adicione o som de clique em 'audio/cliques/click.wav'
4. Adicione a música de fundo em 'audio/musica_fundo/music.mp3'
5. Execute o app com: python main.py
    """)

if __name__ == "__main__":
    criar_pastas()
    criar_arquivos_vazios()
    mostrar_instrucoes()