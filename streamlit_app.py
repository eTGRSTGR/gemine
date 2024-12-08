import streamlit as st
import google.generativeai as genai

# Configuração direta da API
API_KEY = 'AIzaSyCQDgxbYhdgZT3VEgTg7vO33WUkugSbjKs'  # Substitua pelo sua chave real
genai.configure(api_key=API_KEY)


def transcribe_image(uploaded_file):
    """
    Transcreve texto de uma imagem carregada usando Google Generative AI
    """
    try:
        # Cria o modelo
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Inicia sessão de chat com a imagem carregada
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [genai.upload_file(uploaded_file.name, mime_type=uploaded_file.type)]
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
    
    # Carregador de arquivo
    uploaded_file = st.file_uploader(
        "Escolha uma imagem...", 
        type=["png", "jpg", "jpeg", "gif"]
    )
    
    # Se arquivo for carregado
    if uploaded_file is not None:
        # Exibe a imagem carregada - Note a mudança para use_container_width
        st.image(uploaded_file, caption="Imagem Carregada", use_container_width=True)
        
        # Botão de transcrição
        if st.button("Transcrever Texto"):
            # Mostra spinner de carregamento
            with st.spinner("Transcrevendo..."):
                # Chama função de transcrição
                transcription = transcribe_image(uploaded_file)
                
                # Exibe a transcrição
                if transcription:
                    st.success("Transcrição concluída!")
                    st.text_area("Texto Transcrito:", value=transcription, height=200)

# Executa o aplicativo
if __name__ == "__main__":
    main()