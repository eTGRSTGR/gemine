import streamlit as st
import google.generativeai as genai

# Configuração direta da API
API_KEY = 'AIzaSyCQDgxbYhdgZT3VEgTg7vO33WUkugSbjKs'  # Substitua pelo sua chave real
genai.configure(api_key=API_KEY)


def transcribe_image(image):
    """
    Transcreve texto de uma imagem usando Google Generative AI
    """
    try:
        # Converte a imagem para o formato adequado
        pil_image = Image.fromarray(image)
        
        # Salva a imagem temporariamente
        temp_file = "temp_image.png"
        pil_image.save(temp_file)
        
        # Cria o modelo
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Inicia sessão de chat com a imagem carregada
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [genai.upload_file(temp_file, mime_type="image/png")]
                }
            ]
        )
        
        # Envia mensagem para transcrever
        response = chat_session.send_message("Transcreva o que foi escrito na imagem.")
        
        return response.text
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
        return None

def main():
    st.title("Transcrição de Texto com Google Generative AI")
    
    # Escolha do método de entrada de imagem
    opcao = st.radio("Escolha o método de entrada:", 
                     ["Carregar Imagem", "Usar Câmera"])
    
    # Variável para armazenar a imagem
    image = None
    
    if opcao == "Carregar Imagem":
        # Carregador de arquivo tradicional
        uploaded_file = st.file_uploader(
            "Escolha uma imagem...", 
            type=["png", "jpg", "jpeg", "gif"]
        )
        
        if uploaded_file is not None:
            # Converte o arquivo carregado para array numpy
            image = np.array(Image.open(uploaded_file))
            st.image(image, caption="Imagem Carregada", use_container_width=True)
    
    else:
        # Captura de imagem da câmera
        camera_image = st.camera_input("Tire uma foto")
        
        if camera_image is not None:
            # Converte a imagem capturada para array numpy
            image = np.array(Image.open(camera_image))
            st.image(image, caption="Imagem Capturada", use_container_width=True)
    
    # Botão de transcrição
    if image is not None:
        if st.button("Transcrever Texto"):
            # Mostra spinner de carregamento
            with st.spinner("Transcrevendo..."):
                # Chama função de transcrição
                transcription = transcribe_image(image)
                
                # Exibe a transcrição
                if transcription:
                    st.success("Transcrição concluída!")
                    st.text_area("Texto Transcrito:", value=transcription, height=200)

# Executa o aplicativo
if __name__ == "__main__":
    main()
