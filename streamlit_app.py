import streamlit as st
import google.generativeai as genai
import numpy as np
from PIL import Image
import io

# Configuração direta da API
API_KEY = 'AIzaSyCQDgxbYhdgZT3VEgTg7vO33WUkugSbjKs'  # Substitua pelo sua chave real
genai.configure(api_key=API_KEY)


def transcribe_image_with_gemini(image):
    """
    Transcreve texto de uma imagem usando Google Gemini.
    """
    try:
        # Converte a imagem para bytes
        image_bytes = io.BytesIO()
        pil_image = Image.fromarray(image)
        pil_image.save(image_bytes, format='PNG')
        image_bytes.seek(0)
        
        # Envia a imagem para Gemini
        response = genai.upload_file(image_bytes, mime_type="image/png")
        
        # Verifica se a resposta contém texto transcrito
        if hasattr(response, 'text'):
            return response.text
        else:
            return "Nenhum texto encontrado na imagem."
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
        return None

def main():
    st.title("Transcrição de Texto com Google Gemini")
    
    # Escolha do método de entrada de imagem
    opcao = st.radio("Escolha o método de entrada:", 
                     ["Carregar Imagem", "Usar Câmera"])
    
    # Variável para armazenar a imagem
    image = None
    
    if opcao == "Carregar Imagem":
        uploaded_file = st.file_uploader("Escolha uma imagem...", 
                                         type=["png", "jpg", "jpeg"])
        if uploaded_file:
            # Carrega a imagem diretamente de BytesIO
            image = Image.open(uploaded_file)
            image = np.array(image)  # Converte para array NumPy
            st.image(image, caption="Imagem Carregada", use_container_width=True)
    
    else:
        camera_image = st.camera_input("Tire uma foto")
        if camera_image:
            image = np.array(Image.open(camera_image))
            st.image(image, caption="Imagem Capturada", use_container_width=True)
    
    # Botão de transcrição
    if image is not None:
        if st.button("Transcrever Texto"):
            with st.spinner("Transcrevendo..."):
                transcription = transcribe_image_with_gemini(image)
                if transcription:
                    st.success("Transcrição concluída!")
                    st.text_area("Texto Transcrito:", value=transcription, height=200)

if __name__ == "__main__":
    main()
