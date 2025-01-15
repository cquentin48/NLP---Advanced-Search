import streamlit as st
import requests

from urllib.error import HTTPError

API_URL="http://serving:8080/"

def is_api_set():
    """
    Check if the Open Domain QA is up or not.
    If not, an exception is raised
    """
    result = requests.get(API_URL)
    if(not result.ok):
        result.raise_for_status()
        raise HTTPError("",0,"API Down",None,None)

def predict_answer_context(question:str,context:str):
    input = {
        'context':context,
        'question':question
    }
    answer = requests.post(f"{API_URL}ask/context",json=input)
    return answer.json()['answer']

def predict_answer_vector(question:str):
    input = {
        'question':question
    }
    answer = requests.post(f"{API_URL}ask/open",json=input)
    print(answer)
    return answer.json()['answer']

st.set_page_config(page_title="Machine Learning - Open QA")

st.title("Machine Learning - Open QA")

with st.expander(":thinking_face: Plus d'informations sur le projet"):
    st.write(
        "Projet informatique réalisé dans le cadre universitaire. "+
        "Ce projet a été réalisé dans le cadre de la matière \"Machine Learning 2\". "+
        "Il s'agit d'une application répondant à vos question à partir de connaissances.\n"+
        "Son but était de servir de complément au moteur de recherche Qwant si ce dernier"+
        " disposait des connaissances permettant de répondre à la question."
    )

try:
    is_api_set()
except HTTPError as err:
    st.toast("Malheureusement vous ne pouvez pas demander des question car le service n'est pas disponible. Merci de réessayer plus tard.")

chatbox_type = st.selectbox(
    'Choix du modèle',
    ('Basé sur le contexte', 'Basé sur les vecteurs')
)

if chatbox_type == 'Basé sur les vecteurs':
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("✨ Que voulez-vous savoir?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        #response = f"My answer here!"
        response = predict_answer_vector(prompt)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
elif chatbox_type == 'Basé sur le contexte':
    placeholder = st.empty()
    answer_placeholder = placeholder.text_input("Réponse","Réponse du logiciel",disabled=True)
    question = st.text_input("Votre Question","Où est-ce que je vis?")
    context = st.text_area("Contexte","Mon nom est Wolfgang et je vis à Berlin.")
    if st.button("Réponse du bot"):
        bot_answer = predict_answer_context(question,context)
        answer_placeholder = placeholder.text_input("Réponse",bot_answer)
