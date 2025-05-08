# main.py - Albion Lucro Pro (100% Automático)

import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from utils.auto_fix import AutoFixer
from utils.audio import tocar_som_clique, iniciar_musica_fundo
from utils.busca_inteligente import buscar_item_id, buscar_item_semelhante
from features.favoritos import salvar_favorito, carregar_favoritos
from features.crafting import calcular_custo_crafting
from features.metas import salvar_meta, carregar_meta
from features.transporte import simular_custo_transporte
from features.builds import montar_build_simples, salvar_build, carregar_builds_disponiveis, carregar_build

TIERS = ["T4", "T5", "T6", "T7", "T8"]
ENCANTAMENTOS = [".0", ".1", ".2", ".3", ".4"]
QUALIDADES = ["Normal", "Boa", "Excelente", "Obra-prima"]
CIDADES = ["Caerleon", "Martlock", "Lymhurst", "Bridgewatch", "Fort Sterling", "Thetford"]


def verificar_criar_pastas():
    pastas = [
        "assets/fundo", "assets/icones", "assets/botoes", "assets/scrollbar",
        "audio/cliques", "audio/musica_fundo", "data", "config", "logs",
        "data/builds", "data/metas", "data/crafting", "data/transporte",
        "export", "api_cache", "temp", "screenshots"
    ]
    for pasta in pastas:
        os.makedirs(pasta, exist_ok=True)

def montar_item_id(item_base, tier, encantamento):
    enc = encantamento.replace(".0", "")
    return f"{item_base}_{tier}{f'@{enc}' if enc else ''}"

def baixar_icone(item_id):
    url = f"https://render.albiononline.com/v1/item/{item_id}.png"
    caminho = f"assets/icones/{item_id}.png"
    if not os.path.exists(caminho):
        try:
            import requests
            r = requests.get(url)
            if r.status_code == 200:
                with open(caminho, 'wb') as f:
                    f.write(r.content)
        except:
            pass
    return caminho if os.path.exists(caminho) else None

class AppAlbion:
    def __init__(self, root):
        self.root = root
        self.root.title("Albion Lucro Pro v2")
        self.root.geometry("1280x720")
        self.root.configure(bg="#0f0f0f")
        self.root.minsize(1024, 600)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        self.aba_principal = tk.Frame(self.notebook, bg="#0f0f0f")
        self.notebook.add(self.aba_principal, text="🏠 Painel Principal")

        self.carregar_fundo()
        self.carregar_estilo()
        self.criar_filtros()
        self.botao_ver_favoritos()
        self.criar_aba_crafting()
        self.criar_aba_meta()
        self.criar_aba_transporte()
        self.criar_aba_builds()

    def carregar_fundo(self):
        caminho = "assets/fundo/bg_app.png"
        if os.path.exists(caminho):
            imagem = Image.open(caminho).resize((1280, 720))
            img_tk = ImageTk.PhotoImage(imagem)
            label_fundo = tk.Label(self.aba_principal, image=img_tk)
            label_fundo.image = img_tk
            label_fundo.place(x=0, y=0, relwidth=1, relheight=1)

    def carregar_estilo(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("TLabel", foreground="white", background="#0f0f0f")
        estilo.configure("TButton", padding=6, relief="flat",
                         background="#1f1f1f", foreground="white")

    def criar_filtros(self):
        container = tk.Frame(self.aba_principal, bg="#0f0f0f")
        container.pack(padx=15, pady=20, anchor="nw")

        tk.Label(container, text="🧾 Nome do Item:", fg="white", bg="#0f0f0f").grid(row=0, column=0, sticky="w")
        self.entrada_nome = tk.Entry(container, width=30)
        self.entrada_nome.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(container, text="🏷️ Tier:", fg="white", bg="#0f0f0f").grid(row=1, column=0, sticky="w")
        self.box_tier = ttk.Combobox(container, values=TIERS, width=10)
        self.box_tier.set("T7")
        self.box_tier.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(container, text="✨ Encantamento:", fg="white", bg="#0f0f0f").grid(row=2, column=0, sticky="w")
        self.box_encantamento = ttk.Combobox(container, values=ENCANTAMENTOS, width=10)
        self.box_encantamento.set(".2")
        self.box_encantamento.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(container, text="💎 Qualidade:", fg="white", bg="#0f0f0f").grid(row=3, column=0, sticky="w")
        self.box_qualidade = ttk.Combobox(container, values=QUALIDADES, width=14)
        self.box_qualidade.set("Excelente")
        self.box_qualidade.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(container, text="📍 Cidade:", fg="white", bg="#0f0f0f").grid(row=4, column=0, sticky="w")
        self.box_cidade = ttk.Combobox(container, values=CIDADES, width=14)
        self.box_cidade.set("Caerleon")
        self.box_cidade.grid(row=4, column=1, padx=10, pady=5)

        botao_analisar = tk.Button(container, text="🔎 Analisar Item", font=("Arial", 11, "bold"),
                                   bg="#222", fg="#00ffcc", relief="ridge", command=self.executar_analise)
        botao_analisar.grid(row=5, column=0, columnspan=2, pady=15)

    def executar_analise(self):
        nome = buscar_item_semelhante(self.entrada_nome.get())
        tier = self.box_tier.get()
        encantamento = self.box_encantamento.get()
        qualidade = self.box_qualidade.get()
        cidade = self.box_cidade.get()

        resultado = buscar_item_id(nome)
        if not resultado:
            messagebox.showerror("Item não encontrado", "Item não reconhecido. Tente outro nome.")
            return

        item_base, nome_resolvido = resultado

        if not item_base:
            messagebox.showerror("Item não encontrado", "Item não reconhecido. Tente outro nome.")
            return
        item_id = f"{tier}_{item_base}{('@'+encantamento.replace('.0', '')) if encantamento != '.0' else ''}"
        icone_path = baixar_icone(item_id)

        nova_aba = tk.Frame(self.notebook, bg="#151515")
        self.notebook.add(nova_aba, text=f"📦 {item_id}")
        self.notebook.select(nova_aba)

        if icone_path:
            img = Image.open(icone_path).resize((64, 64))
            img_tk = ImageTk.PhotoImage(img)
            icone = tk.Label(nova_aba, image=img_tk, bg="#151515")
            icone.image = img_tk
            icone.pack(pady=15)

        label = tk.Label(nova_aba, text=f"Analisando: {item_id}\nQualidade: {qualidade}\nCidade: {cidade}",
                         bg="#151515", fg="white", font=("Arial", 12))
        label.pack(pady=10)

        btn_favorito = tk.Button(nova_aba, text="⭐ Adicionar aos Favoritos",
                                 command=lambda: salvar_favorito(item_id, nome, qualidade, cidade),
                                 bg="#333", fg="gold")
        btn_favorito.pack(pady=10)

    def botao_ver_favoritos(self):
        botao = tk.Button(self.aba_principal, text="⭐ Ver Favoritos", command=self.abrir_favoritos,
                          bg="#222", fg="gold")
        botao.pack(anchor="ne", padx=20, pady=5)

    def abrir_favoritos(self):
        favoritos = carregar_favoritos()
        aba_fav = tk.Frame(self.notebook, bg="#1a1a1a")
        self.notebook.add(aba_fav, text="⭐ Favoritos")
        self.notebook.select(aba_fav)

        for fav in favoritos:
            item_txt = f"{fav['nome']} - {fav['id']} - {fav['cidade']} ({fav['qualidade']})"
            btn = tk.Button(aba_fav, text=item_txt, width=80, command=lambda f=fav: self.executar_analise_fav(f))
            btn.pack(pady=4)

    def executar_analise_fav(self, fav):
        self.entrada_nome.delete(0, tk.END)
        self.entrada_nome.insert(0, fav['nome'])
        self.box_qualidade.set(fav['qualidade'])
        self.box_cidade.set(fav['cidade'])
        self.executar_analise()

    def criar_aba_crafting(self):
        aba = tk.Frame(self.notebook, bg="#101010")
        self.notebook.add(aba, text="⚒️ Crafting e Refino")

        tk.Label(aba, text="Item:", bg="#101010", fg="white").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        entry_item = tk.Entry(aba, width=25)
        entry_item.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(aba, text="Quantidade:", bg="#101010", fg="white").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        entry_qtd = tk.Entry(aba, width=10)
        entry_qtd.insert(0, "1")
        entry_qtd.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(aba, text="Taxa da Cidade (%):", bg="#101010", fg="white").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        entry_taxa = tk.Entry(aba, width=10)
        entry_taxa.insert(0, "18")
        entry_taxa.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(aba, text="Retorno com Foco (%):", bg="#101010", fg="white").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        entry_retorno = tk.Entry(aba, width=10)
        entry_retorno.insert(0, "48")
        entry_retorno.grid(row=3, column=1, padx=10, pady=5)

        resultado_label = tk.Label(aba, text="", bg="#101010", fg="lime")
        resultado_label.grid(row=5, column=0, columnspan=2, pady=10)

        def calcular_custo():
            try:
                qtd = int(entry_qtd.get())
                taxa = float(entry_taxa.get()) / 100
                retorno = float(entry_retorno.get()) / 100
                custo = calcular_custo_crafting(qtd, taxa, retorno)
                resultado_label.config(text=f"💰 Custo final: {custo} prata")
            except Exception as e:
                resultado_label.config(text=f"Erro: {str(e)}", fg="red")

        btn_calcular = tk.Button(aba, text="🧮 Calcular", bg="#222", fg="white", command=calcular_custo)
        btn_calcular.grid(row=4, column=0, columnspan=2, pady=10)

    def criar_aba_meta(self):
        pass

    def criar_aba_transporte(self):
        pass

    def criar_aba_builds(self):
        pass

if __name__ == "__main__":
    verificar_criar_pastas()
    try:
        fixer = AutoFixer()
        print(fixer.diagnostico_geral())
    except Exception as e:
        print(f"Erro ao verificar estrutura: {e}")
    root = tk.Tk()
    app = AppAlbion(root)
    try:
        iniciar_musica_fundo()
    except:
        pass
    root.mainloop()