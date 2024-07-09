# streamlit -> 프론트앤드 라이브러리
import streamlit as st
# os모듈 불러오기 -> 환경변수값 얻기 위해 불러오기
import os
# openai의 API(application programming interface) client 사용하기 위한 모듈 불러오기
from openai import OpenAI
#.env 파일 -> 환경변수 불러오기
from dotenv import load_dotenv
import pyaudio
import wave
# JSON파일에 있는 데이터를 다루기 위해 쓰는 모듈
import json

# gpt-4o모델 사용하기
MODEL="gpt-4o"
# 환경변수에서 api_key를 가져와서 openai class의 객체를 만듬
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as an env var>"))

# .env파일에서 환경 변수 불러오기
load_dotenv()


# Conversation_Data.json 파일을 읽어서 DataFrame으로 변환
# json파일을 읽어서 f로 사용하겠다..~ <<file handle - fp : file pointer>>
with open('Conversation_Data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    
# 데이터 형식을  str로 변환하겠다..~(한글 안깨지게 하기 위해 사용) / indent=4 -> 들여쓰기 4칸  
data_str = json.dumps(data, ensure_ascii=False, indent=4)

# AI가 참조할 수 있게 프롬프팅
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
    # gpt model -> client의 질문에 따라 요청과 응답..
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