import os
from PIL import Image, ImageDraw, ImageFont
import streamlit as st

# ==============================================================================
# BLOCO DE CONFIGURAÇÃO DO CRACHÁ DA SHELL
# (Configuração base, não precisa mexer)
# ==============================================================================
CONFIG_SHELL = {
    "arquivo_template": os.path.join(os.path.dirname(__file__), "static", "template_shell.jpg"),
    "fonte": os.path.join(os.path.dirname(__file__), "arialbd.ttf"),
    "cor_texto": "black",
    "tamanhos_fonte": {
        "nome": 40,
        "dados": 35
    },
    "coordenadas": {
        "nome": (50, 175),
        "rg": (50, 225),
        "cpf": (50, 275),
        "foto": (220, 340)
    },
    "tamanho_foto": (225, 240)
}

# ==============================================================================
# BLOCO DE CONFIGURAÇÃO DO CRACHÁ DA CAIXA (COM AS CORREÇÕES)
# As coordenadas estão ajustadas para posicionar o texto ABAIXO da foto.
# ==============================================================================
CONFIG_CAIXA = {
    # ATENÇÃO: Verifique se o nome do seu arquivo de template está correto aqui.
    "arquivo_template": os.path.join(os.path.dirname(__file__), "static", "Crachá empresarial com foto e informações simples azul verde e branco.png"),
    "fonte": os.path.join(os.path.dirname(__file__), "arialbd.ttf"),
    "cor_texto": (255, 255, 255),  # Branco
    "tamanhos_fonte": {
        "nome": 40,
        "dados": 35
    },
    "coordenadas": {
        "nome": (233,515,398,464),  # Coordenada corrigida
        "rg":   (180, 465),  # Coordenada corrigida
        "cpf":  (180, 515),  # Coordenada corrigida
        "foto": (213, 222)
    },
    "tamanho_foto": (174, 174)
}


# --- FUNÇÕES ---

def carregar_fonte(caminho_fonte, tamanho):
    try:
        if not os.path.exists(caminho_fonte):
            caminho_fonte = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        return ImageFont.truetype(caminho_fonte, tamanho)
    except Exception as e:
        st.error(f"Erro ao carregar a fonte: {e}")
        raise

# --- Função principal de geração (COM A CORREÇÃO NO TEXTO) ---
def gerar_cracha(nome, rg, cpf, template_escolhido, foto_path=None):
    try:
        if template_escolhido == "Shell":
            config = CONFIG_SHELL
        else: # "Caixa"
            config = CONFIG_CAIXA

        if not os.path.exists(config["arquivo_template"]):
            raise FileNotFoundError(f"Template não encontrado: {config['arquivo_template']}")
        
        template = Image.open(config["arquivo_template"])
        draw = ImageDraw.Draw(template)

        fonte_nome = carregar_fonte(config["fonte"], config["tamanhos_fonte"]["nome"])
        fonte_dados = carregar_fonte(config["fonte"], config["tamanhos_fonte"]["dados"])

        # --- TEXTO CORRIGIDO (SEM PREFIXOS "Nome:", "RG:", "CPF:") ---
        draw.text(config["coordenadas"]["nome"], nome, fill=config["cor_texto"], font=fonte_nome)
        draw.text(config["coordenadas"]["rg"], rg, fill=config["cor_texto"], font=fonte_dados)
        draw.text(config["coordenadas"]["cpf"], cpf, fill=config["cor_texto"], font=fonte_dados)

        if foto_path:
            try:
                foto = Image.open(foto_path).resize(config["tamanho_foto"])
                template.paste(foto, config["coordenadas"]["foto"])
            except Exception as e:
                st.error(f"Erro ao processar a foto: {e}")

        output_path = f"cracha_gerado_{template_escolhido.lower()}.png"
        template.save(output_path)
        return output_path

    except Exception as e:
        st.error(f"Erro ao gerar o crachá: {e}")
        return None

# --- INTERFACE STREAMLIT ---

st.title("Gerador de Crachás")

escolha_template = st.selectbox(
    "Escolha o Template:",
    ("Shell", "Caixa")
)

nome = st.text_input("Nome:")
rg = st.text_input("RG:")
cpf = st.text_input("CPF:")
foto = st.file_uploader("Envie uma foto (opcional):", type=["jpg", "jpeg", "png"])

if not os.path.exists("static"):
    os.makedirs("static")

if st.button("Gerar Crachá"):
    if nome and rg and cpf:
        foto_path = None
        if foto:
            foto_path = os.path.join("static", "foto_temp.jpg")
            with open(foto_path, "wb") as f:
                f.write(foto.getbuffer())
        
        output_path = gerar_cracha(nome, rg, cpf, escolha_template, foto_path)
        
        if output_path:
            st.success("Crachá gerado com sucesso!")
            st.image(output_path)
    else:
        st.error("Por favor, preencha todos os campos obrigatórios.")
