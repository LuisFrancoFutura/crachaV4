import os
from PIL import Image, ImageDraw, ImageFont
import streamlit as st

# ==============================================================================
# BLOCO DE CONFIGURAÇÃO DO CRACHÁ DA SHELL
# (Valores de exemplo baseados no seu código original)
# ==============================================================================
CONFIG_SHELL = {
    "arquivo_template": os.path.join(os.path.dirname(__file__), "static", "template_shell.jpg"),
    "fonte": os.path.join(os.path.dirname(__file__), "arialbd.ttf"),
    "cor_texto": "black",
    "tamanhos_fonte": {
        "nome": 40,
        "dados": 35  # Para RG e CPF
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
# BLOCO DE CONFIGURAÇÃO DO CRACHÁ DA CAIXA (EDITAR AQUI)
# Altere os valores abaixo de acordo com o seu novo template da Caixa.
# ==============================================================================
CONFIG_CAIXA = {
    "arquivo_template": os.path.join(os.path.dirname(__file__), "static", "template_caixa.jpg"),
    "fonte": os.path.join(os.path.dirname(__file__), "futura.ttf"), # Exemplo: outra fonte
    "cor_texto": (0, 92, 169),  # Exemplo: Azul Caixa
    "tamanhos_fonte": {
        "nome": 45,
        "dados": 38
    },
    "coordenadas": {
        # !!! Use um editor de imagem (Paint) para achar os valores (X, Y) corretos !!!
        "nome": (65, 480),
        "rg": (65, 530),
        "cpf": (65, 580),
        "foto": (250, 150)
    },
    "tamanho_foto": (200, 250)
}

# --- FUNÇÕES (MODIFICADAS PARA USAR AS CONFIGURAÇÕES) ---

def carregar_fonte(caminho_fonte, tamanho):
    try:
        # Verifica se o caminho da fonte existe, senão usa uma alternativa
        if not os.path.exists(caminho_fonte):
            caminho_fonte = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        return ImageFont.truetype(caminho_fonte, tamanho)
    except Exception as e:
        st.error(f"Erro ao carregar a fonte: {e}")
        raise

# --- Função principal de geração, agora mais flexível ---
def gerar_cracha(nome, rg, cpf, template_escolhido, foto_path=None):
    try:
        # 1. Carrega a configuração correta baseada na escolha do usuário
        if template_escolhido == "Shell":
            config = CONFIG_SHELL
        else: # "Caixa"
            config = CONFIG_CAIXA

        # 2. Abre o arquivo de template correto
        if not os.path.exists(config["arquivo_template"]):
            raise FileNotFoundError(f"Template não encontrado: {config['arquivo_template']}")
        
        template = Image.open(config["arquivo_template"])
        draw = ImageDraw.Draw(template)

        # 3. Carrega as fontes com os tamanhos corretos
        fonte_nome = carregar_fonte(config["fonte"], config["tamanhos_fonte"]["nome"])
        fonte_dados = carregar_fonte(config["fonte"], config["tamanhos_fonte"]["dados"])

        # 4. Usa as coordenadas e cores corretas
        draw.text(config["coordenadas"]["nome"], f"Nome: {nome}", fill=config["cor_texto"], font=fonte_nome)
        draw.text(config["coordenadas"]["rg"], f"RG: {rg}", fill=config["cor_texto"], font=fonte_dados)
        draw.text(config["coordenadas"]["cpf"], f"CPF: {cpf}", fill=config["cor_texto"], font=fonte_dados)

        # 5. Adiciona a foto, se fornecida
        if foto_path:
            try:
                foto = Image.open(foto_path).resize(config["tamanho_foto"])
                template.paste(foto, config["coordenadas"]["foto"])
            except Exception as e:
                st.error(f"Erro ao processar a foto: {e}")

        # 6. Salva o crachá gerado
        output_path = f"cracha_gerado_{template_escolhido.lower()}.png"
        template.save(output_path)
        return output_path

    except Exception as e:
        st.error(f"Erro ao gerar o crachá: {e}")
        return None

# --- INTERFACE STREAMLIT ---

st.title("Gerador de Crachás")

# +++ ADICIONADO: SELEÇÃO DE TEMPLATE +++
escolha_template = st.selectbox(
    "Escolha o Template:",
    ("Shell", "Caixa")
)

# Entrada de dados do usuário (sem alteração)
nome = st.text_input("Nome:")
rg = st.text_input("RG:")
cpf = st.text_input("CPF:")
foto = st.file_uploader("Envie uma foto (opcional):", type=["jpg", "jpeg", "png"])

# Criar a pasta 'static' se não existir
if not os.path.exists("static"):
    os.makedirs("static")

# Botão para gerar o crachá
if st.button("Gerar Crachá"):
    if nome and rg and cpf:
        foto_path = None
        if foto:
            foto_path = os.path.join("static", "foto_temp.jpg")
            with open(foto_path, "wb") as f:
                f.write(foto.getbuffer())
        
        # --- MODIFICADO: Passa a escolha do usuário para a função ---
        output_path = gerar_cracha(nome, rg, cpf, escolha_template, foto_path)
        
        if output_path:
            st.success("Crachá gerado com sucesso!")
            st.image(output_path)
    else:
        st.error("Por favor, preencha todos os campos obrigatórios.")
