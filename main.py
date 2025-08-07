import streamlit as st # Importa la librería Streamlit para construir la interfaz web
from langchain import PromptTemplate # Importa PromptTemplate para crear plantillas de instrucciones para el LLM
from langchain_openai import OpenAI # Importa la clase OpenAI para conectarse con el modelo de lenguaje de OpenAI

# Define una plantilla de texto (prompt) para que el modelo reescriba el contenido con el tono y dialecto indicados
template = """
    Below is a draft text that may be poorly worded.
    Your goal is to:
    - Properly redact the draft text
    - Convert the draft text to a specified tone
    - Convert the draft text to a specified dialect

    Here are some examples different Tones:
    - Formal: Greetings! OpenAI has announced that Sam Altman is rejoining the company as its Chief Executive Officer. After a period of five days of conversations, discussions, and deliberations, the decision to bring back Altman, who had been previously dismissed, has been made. We are delighted to welcome Sam back to OpenAI.
    - Informal: Hey everyone, it's been a wild week! We've got some exciting news to share - Sam Altman is back at OpenAI, taking up the role of chief executive. After a bunch of intense talks, debates, and convincing, Altman is making his triumphant return to the AI startup he co-founded.  

    Here are some examples of words in different dialects:
    - American: French Fries, cotton candy, apartment, garbage, \
        cookie, green thumb, parking lot, pants, windshield
    - British: chips, candyfloss, flag, rubbish, biscuit, green fingers, \
        car park, trousers, windscreen

    Example Sentences from each dialect:
    - American: Greetings! OpenAI has announced that Sam Altman is rejoining the company as its Chief Executive Officer. After a period of five days of conversations, discussions, and deliberations, the decision to bring back Altman, who had been previously dismissed, has been made. We are delighted to welcome Sam back to OpenAI.
    - British: On Wednesday, OpenAI, the esteemed artificial intelligence start-up, announced that Sam Altman would be returning as its Chief Executive Officer. This decisive move follows five days of deliberation, discourse and persuasion, after Altman's abrupt departure from the company which he had co-established.

    Please start the redaction with a warm introduction. Add the introduction \
        if you need to.
    
    Below is the draft text, tone, and dialect:
    DRAFT: {draft}
    TONE: {tone}
    DIALECT: {dialect}

    YOUR {dialect} RESPONSE:
"""
# Crea un objeto PromptTemplate a partir de la plantilla anterior, especificando las variables que se llenarán dinámicamente
#PromptTemplate variables definition
prompt = PromptTemplate(
    input_variables=["tone", "dialect", "draft"],
    template=template,
)

# Función para cargar el modelo LLM con la clave de API de OpenAI
#LLM and key loading function
def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Se establece el modelo con una temperatura de 0.7 y se le pasa la clave API
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

# Establece la configuración de la página web de Streamlit
#Page title and header
st.set_page_config(page_title="Re-write your text")
# Muestra un título principal en la aplicación
st.header("Re-write your text")

# Divide la pantalla en dos columnas para mostrar instrucciones e información de contacto
#Intro: instructions
col1, col2 = st.columns(2)

with col1:
    st.markdown("Re-write your text in different styles.")

with col2:
    st.write("Contact with [AI Accelera](https://aiaccelera.com) to build your AI Projects")

# Sección para ingresar la clave API de OpenAI
#Input OpenAI API Key
st.markdown("## Enter Your OpenAI API Key")

# Función que muestra un input oculto para ingresar la clave API
def get_openai_api_key():
    input_text = st.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input", type="password")
    return input_text

# Obtiene la clave API desde el input del usuario
openai_api_key = get_openai_api_key()

# Sección para ingresar el texto a reescribir
# Input
st.markdown("## Enter the text you want to re-write")

# Función que crea un área de texto para ingresar el contenido
def get_draft():
    draft_text = st.text_area(label="Text", label_visibility='collapsed', placeholder="Your Text...", key="draft_input")
    return draft_text

# Guarda el texto ingresado por el usuario
draft_input = get_draft()

# Si el texto tiene más de 700 palabras, se detiene la app
if len(draft_input.split(" ")) > 700:
    st.write("Please enter a shorter text. The maximum length is 700 words.")
    st.stop()

# Sección para elegir el tono y el dialecto del texto reescrito
# Prompt template tunning options
col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox(
        'Which tone would you like your redaction to have?',
        ('Formal', 'Informal'))
    
with col2:
    option_dialect = st.selectbox(
        'Which English Dialect would you like?',
        ('American', 'British'))
    
# Título para la sección de resultado
# Output
st.markdown("### Your Re-written text:")

# Si hay texto ingresado...
if draft_input:
    if not openai_api_key: # ...pero no hay clave API, muestra advertencia y detiene la app
        st.warning('Please insert OpenAI API Key. \
            Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', 
            icon="⚠️")
        st.stop()
# Carga el modelo con la clave API
    llm = load_LLM(openai_api_key=openai_api_key)
 
 # Llena la plantilla con los datos del usuario
    prompt_with_draft = prompt.format(
        tone=option_tone, 
        dialect=option_dialect, 
        draft=draft_input
    )

 # Ejecuta el modelo y obtiene el resultado
    improved_redaction = llm(prompt_with_draft)

 # Muestra el texto reescrito en pantalla
    st.write(improved_redaction)