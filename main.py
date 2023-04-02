import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

template = """
    Te voy a dar un email que no esta bien escrito.
    Tus objetivos son:
    - Escribir el email en el formato correcto
    - Convertir el texto de input a un tono adecuado
    - Convertir el texto a un dialecto adecuado
    - Hacer que exista separacion entre sentencias de ser necesario
    Aqui te dejo ejemplos de distintos tonos:
    - Formal: Fuimos a Jamaica el finde semana. Tenemos muchas cosas que contarte.
    - Informal: Nos pasamos por Barcelona el finde. Tenemos que hablar.  
    Aqui te dejo unos ejemplos de palabras para diferentes dialectos:
    - Argentino: abriojo, anteojos, aplanadora, estacionar, faso, figurita, gaseosa, guaso, intendente
    - Español: velcro, Gafas, apisonadora, aparca, cigarrillo, cromo, refresco, guarro, alcalde
    Ejemplo de cada dialecto:
    - Argentino: Un pibe con un buzo celeste y con olor a escabio se llevo mi celular un chorro justo cobre de una changa una luca que necesitaba para pagar el bondi
    - Español: Un chico con una sudadera celeste y oliendo a alcohol me robó mi celular justo después de que cobré mil pesos por un trabajo temporal que necesitaba para pagar el autobús
    
    Debajo esta el email, tono y dialecto:
    TONO: {tono}
    DIALECTO: {dialecto}
    EMAIL: {email}
    
    TU RESPUESTA {dialecto} :
"""

prompt = PromptTemplate(
    input_variables=["tono", "dialecto", "email"],
    template=template,
)

def load_LLM(openai_api_key):
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="Escribe Emails Facilmente", page_icon=":robot:")
st.header("Escribir emails nunca fue mas facil")

col1, col2 = st.columns(2)

with col1:
    st.markdown("Si te sirve para algo y quieres seguir apoyandome dejame un comentario y un like en el video \n\n Aqui te dejo el link:")



st.markdown("## Escribe el Email que quieres convertir")

openai_api_key = ""

col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox(
        'Que tono quieres?',
        ('Formal', 'Informal'))
    
with col2:
    option_dialect = st.selectbox(
        'Que dialecto quieres?',
        ('Español', 'Argentino'))

def get_text():
    input_text = st.text_area(label="Email Input", label_visibility='collapsed', placeholder="Tu Email...Una vez escrito presiona CRTL + ENTER", key="email_input")
    return input_text

email_input = get_text()

if len(email_input.split(" ")) > 700:
    st.write("Por favor introudce un mail mas corto. El maximo son 700 palabras.")
    st.stop()

def update_text_with_example():
    print ("in updated")
    st.session_state.email_input = "Jose empiezo este lunes a trabajr contigo"

st.button("*Mira un ejemplo*", type='secondary', help="Mira un ejemplo de como funciona.", on_click=update_text_with_example)

st.markdown("### Has convertido tu email:")

if email_input:
    if not openai_api_key:
        st.warning('Escribe tu OpenAI API Key. Las instrucciones estan [aqui](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_email = prompt.format(tono=option_tone, dialecto=option_dialect, email=email_input)

    formatted_email = llm(prompt_with_email)

    st.write(formatted_email)