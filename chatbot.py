import streamlit as st  
import os  
from openai import OpenAI
from dotenv import load_dotenv

MODEL="gpt-4o"
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as an env var>"))


load_dotenv()

st.title("Streamlit ChatGPT")


if 'messages' not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['content'])

with st.form(key='chat_form'):
    user_message = st.text_input("User:")
    submit_button = st.form_submit_button(label='Send')

if submit_button and user_message:
    st.session_state.messages.append({"role": "user", "content": user_message})  

    completion = client.chat.completions.create(
        model=MODEL,
        messages=st.session_state.messages,
    )
    response = completion.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": response})

    st.experimental_rerun()