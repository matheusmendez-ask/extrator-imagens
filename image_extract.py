import streamlit as st
import google.generativeai as genai
from PIL import Image

genai.configure(api_key="AIzaSyAQtVEv2cg-N1basqVdEcm8wbIhoGWT1Uo")

# Iniciando o Modelo
def initialize_model(model_name="gemini-pro-vision"):
    model = genai.GenerativeModel(model_name)
    return model

# Configuração da página
st.set_page_config(page_title="Extrator de Imagens", layout="wide")

# Título e descrição
st.title("Extrator de Imagens")
st.write("Este aplicativo extrai imagens com base em um prompt usando CLIP e BigGAN.")

# Entrada do prompt
prompt = st.text_area("Digite seu prompt", height=100)

# Upload da imagem
uploaded_image = st.file_uploader("Escolha uma imagem (jpg, png, jpeg)", type=["jpg", "png", "jpeg"])

def get_image_bytes(uploaded_image):
    if uploaded_image is not None:
        # Leia a imagem enviada em bytes
        image_bytes = uploaded_image.getvalue()

        image_info = [
            {
            "mime_type": uploaded_image.type,
            "data": image_bytes
        }
        ]
        return image_info
    else:
        raise FileNotFoundError("Carregar arquivo de imagem válido!")

def get_response(model, model_behavior, image, prompt):
    response = model.generate_content([model_behavior, image[0], prompt])
    return response.text

# Inicialize o gemini-pro-vision
model = initialize_model("gemini-pro-vision")

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Sua imagem", use_column_width=True)

# create submit button, to submit image along with image
submit = st.button("Enviar")

# set the model behavior
model_behavior = """
Você é um especialista que entende as estruturas gerais das imagens e tem profundo conhecimento sobre elas.
Faremos o upload de imagens e você deverá responder à pergunta com base nas informações
presente na imagem que você ver.
"""

# Se o usuário pressionou o botão enviar
if submit or prompt:
    if len(prompt) > 0:
        # obter arquivo de imagem carregado em bytes
        image_info = get_image_bytes(uploaded_image)
        response = get_response(model, model_behavior, image_info, prompt)
        st.write(response)
    else:
        raise ValueError("Por favor, insira um prompt válido!")