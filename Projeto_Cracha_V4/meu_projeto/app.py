# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont

# ==============================================================================
# CONFIGURAÇÕES DO CRACHÁ DA SHELL (NÃO MEXER AQUI)
# Estas são as configurações que você disse que já estão funcionando.
# ==============================================================================
CONFIG_SHELL = {
    "arquivo_template": "templates/template_shell.png",
    "cor_texto": (0, 0, 0),  # Preto
    "fonte": "fonts/Verdana.ttf",
    "tamanho_fonte": 28,
    "coordenadas": {
        "foto": (50, 50),
        "nome": (250, 150),
        "cargo": (250, 200)
    }
}

# ==============================================================================
# CONFIGURAÇÕES DO CRACHÁ DA CAIXA (EDITAR AQUI)
# Altere os valores abaixo de acordo com o seu novo template da Caixa.
# ==============================================================================
CONFIG_CAIXA = {
    "arquivo_template": "templates/template_caixa.png",
    "cor_texto": (0, 92, 169),  # Exemplo: Azul Caixa
    "fonte": "fonts/Futura.ttf",
    "tamanho_fonte": 32,
    "coordenadas": {
        # !!! Use um editor de imagem (Paint) para achar os valores (X, Y) corretos !!!
        "foto": (65, 200),
        "nome": (65, 480),
        "cargo": (65, 530)
    }
}


# --- Janela Principal ---
root = tk.Tk()
root.title("Gerador de Crachás")
root.geometry("400x350")

# --- Variáveis Globais ---
caminho_foto = ""
template_selecionado = tk.StringVar(value="shell")

# --- Funções ---
def selecionar_foto():
    global caminho_foto
    caminho_foto = filedialog.askopenfilename(
        title="Selecione uma foto",
        filetypes=(("Arquivos de imagem", "*.jpg;*.jpeg;*.png"),)
    )
    if caminho_foto:
        label_foto_status.config(text="Foto selecionada!", fg="green")

def gerar_cracha():
    nome = entry_nome.get()
    cargo = entry_cargo.get()
    escolha = template_selecionado.get()

    if not all([nome, cargo, caminho_foto]):
        label_gerador_status.config(text="Preencha todos os campos e selecione uma foto!", fg="red")
        return

    try:
        # --- LÓGICA DE GERAÇÃO MODIFICADA ---
        # Agora, usamos um if/else para carregar a configuração correta
        # de forma totalmente separada.
        if escolha == "shell":
            config = CONFIG_SHELL
        else: # if escolha == "caixa":
            config = CONFIG_CAIXA

        # O resto do código é genérico e funciona com a 'config' carregada
        cracha = Image.open(config["arquivo_template"])
        draw = ImageDraw.Draw(cracha)
        
        fonte = ImageFont.truetype(config["fonte"], size=config["tamanho_fonte"])
        cor = config["cor_texto"]
        
        coord_nome = config["coordenadas"]["nome"]
        coord_cargo = config["coordenadas"]["cargo"]
        coord_foto = config["coordenadas"]["foto"]

        draw.text(coord_nome, nome, fill=cor, font=fonte)
        draw.text(coord_cargo, cargo, fill=cor, font=fonte)

        foto = Image.open(caminho_foto)
        foto = foto.resize((150, 200))
        cracha.paste(foto, coord_foto)

        nome_arquivo = f"output/cracha_{nome.replace(' ', '_')}_{escolha}.png"
        cracha.save(nome_arquivo)
        
        label_gerador_status.config(text=f"Crachá salvo!", fg="blue")

    except Exception as e:
        label_gerador_status.config(text=f"Ocorreu um erro: {e}", fg="red")


# --- Interface Gráfica (sem alterações) ---
frame_escolha = tk.Frame(root)
frame_escolha.pack(pady=(10,0))
label_escolha = tk.Label(frame_escolha, text="Escolha o Template:")
label_escolha.pack(side=tk.LEFT, padx=5)
radio_shell = tk.Radiobutton(frame_escolha, text="Shell", variable=template_selecionado, value="shell")
radio_shell.pack(side=tk.LEFT)
radio_caixa = tk.Radiobutton(frame_escolha, text="Caixa", variable=template_selecionado, value="caixa")
radio_caixa.pack(side=tk.LEFT)

label_nome = tk.Label(root, text="Nome:")
label_nome.pack(pady=(10, 0))
entry_nome = tk.Entry(root, width=40)
entry_nome.pack()

label_cargo = tk.Label(root, text="Cargo:")
label_cargo.pack(pady=(10, 0))
entry_cargo = tk.Entry(root, width=40)
entry_cargo.pack()

btn_foto = tk.Button(root, text="Selecionar Foto", command=selecionar_foto)
btn_foto.pack(pady=10)
label_foto_status = tk.Label(root, text="")
label_foto_status.pack()

btn_gerar = tk.Button(root, text="Gerar Crachá", command=gerar_cracha)
btn_gerar.pack(pady=10)
label_gerador_status = tk.Label(root, text="")
label_gerador_status.pack()

root.mainloop()
