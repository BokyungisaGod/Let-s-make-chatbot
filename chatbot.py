import streamlit as st  
import os  
from openai import OpenAI
from dotenv import load_dotenv
# import pyaudio
# import wave
import json

MODEL="gpt-4o"
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as an env var>"))


load_dotenv()

# Conversation_Data.json 파일을 읽어서 DataFrame으로 변환
with open('Conversation_Data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


data_str = json.dumps(data, ensure_ascii=False, indent=4)

prompt = f"""당신의 역할은 사용자가 질문을 할 때 데이터의 내용을 참고하여 답변을 하는 것입니다.
데이터에 없는 내용은 답하지 마세요.

데이터: {data_str}"""

if 'backup' not in st.session_state:
    st.session_state.backup = {}


st.title("Streamlit ChatGPT")


if 'messages' not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['content'])

with st.form(key='chat_form'):
    user_message = st.text_input("User:")

    if st.session_state.messages == []:
        user_message = prompt

    submit_button = st.form_submit_button(label='Send')

if submit_button and user_message:
    st.session_state.messages.append({"role": "user", "content": user_message})
    if st.session_state.backup != {}:
        st.session_state.messages[0] = st.session_state.backup

    completion = client.chat.completions.create(
        model=MODEL,
        messages=st.session_state.messages,
    )

    if len(st.session_state.messages) == 1:
        st.session_state.backup = st.session_state.messages[0]
        st.session_state.messages = []
        st.session_state.messages.append({"role": "user", "content": "나의 질문에 답해주세요."})

    if st.session_state.backup != {}:
        st.session_state.messages[0] = {"role": "user", "content": "나의 질문에 답해주세요."}

    response = completion.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": response})

    st.experimental_rerun()