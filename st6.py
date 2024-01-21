# pip install --upgrade openai embedchain streamlit streamlit_chat together docx2txt dotenv
from embedchain import App
import streamlit as st
from streamlit_chat import message

from dotenv import load_dotenv
import os

# Load the environment variables from .env file
load_dotenv()

# Now you can access the environment variables using os.environ
openai_api_key = os.environ['OPENAI_API_KEY']
together_api_key = os.environ['TOGETHER_API_KEY']

# avatar image von Webadresse laden
ray = st.image("https://d8wyob5mxqc1u.cloudfront.net/Allgemein/RaimundBauer180pxMagenta.png", width=80)

# Funktion namens Upload zum Upload aller Dateien im Ordner
def upload():

    # Pfad zum Ordner mit den Daten
    data_folder = 'upload'

    # Durchlaufen aller Dateien im Ordner
    for filename in os.listdir(data_folder):
        # Überprüfen, ob die Datei eine DOC-Datei ist
        if filename.endswith('.docx'):
            # Vollständigen Pfad zur Datei erstellen
            file_path = os.path.join(data_folder, filename)
            # Datei zu app hinzufügen
            crowd_bot.add(file_path, data_type="docx")
    # Überprüfen, ob die Datei eine PDF-Datei ist
        if filename.endswith('.pdf'):
            # Vollständigen Pfad zur Datei erstellen
            file_path = os.path.join(data_folder, filename)
            # Datei zu app hinzufügen
            crowd_bot.add(file_path, data_type="pdf_file")
    # Überprüfen, ob die Datei eine TXT-Datei ist
        if filename.endswith('.txt'):
            # Vollständigen Pfad zur Datei erstellen
            file_path = os.path.join(data_folder, filename)
            # Datei zu app hinzufügen
            crowd_bot.add(file_path, data_type="text")


# from embedchain import OpenSourceApp
st.title ("Crowd-GPT")

def inizialize_session_state():
    if "history" not in st.session_state:
        st.session_state['history'] = []
    if 'generated' not in  st.session_state:
        st.session_state['generated'] = []
    if "past" not in st.session_state:
        st.session_state['past'] = ["Hallo!"]

# initialize the App
crowd_bot = App.from_config(config_path="config.yaml")

# initialize session state
inizialize_session_state()

# get user input for URLs
num_links = st.number_input("Wie viele Links willst Du hinzufügen?", min_value=1, max_value=10, value=1, step=1)
url_inputs =[]

# allow without URLs
try_without_url = st.checkbox("Versuche es ohne Quelle", key="checkbox")

for i in range(num_links):
    url = st.text_input(f" Link {i+1} eingeben", key=f'url_{i}')
    url_inputs.append(url)

# add urls to app instance
for url in url_inputs:
    if url:
        crowd_bot.add("web_page",url)

# conversation chat function
def conversation_chat(query):
    result = crowd_bot.query(query)
    st.session_state['history'].append((query, result))
    return result



def display_chat_history():
    reply_container = st.container()
    container = st.container()

    with container:
        with st.form(key='my_form',clear_on_submit=True):
            user_input = st.text_input(label='Deine Frage', placeholder='Schreibe hier deine Frage',key='input')
            submit_button = st.form_submit_button(label='Absenden')


        if submit_button and user_input:
            if (url):
                output = conversation_chat(user_input)
                st.session_state['past'].append(user_input)
                st.session_state['generated'].append(output)
            elif try_without_url:
                output = conversation_chat(user_input)
                st.session_state['past'].append(user_input)
                st.session_state['generated'].append(output)
            else:
                st.info("Bitte gib einen Link zur Quelle ein (z.B. von Wikipedia)")

        if st.session_state['generated']:
            with reply_container:
                for i in range(len(st.session_state['generated'])):
                    message(st.session_state['past'][i],is_user=True,key=str(i)+"_user",avatar_style="fun-emoji")
                    message(st.session_state['generated'][i], key = str(i), avatar_style="fun-emoji")



# display chat history
display_chat_history()