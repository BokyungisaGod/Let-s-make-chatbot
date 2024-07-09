from flask import Flask, request, jsonify
import openai
import whisper
import kiwipiepy
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
from dotenv import load_dotenv


# 환경 변수 로드
load_dotenv()
app = Flask(__name__)


# Whisper 모델 로드
whisper_model = whisper.load_model('base')

# Kiwi 리트리버 엔진 설정
kiwi = kiwipiepy.Kiwi()

# STT 함수
def speech_to_text(audio_path):
    result = whisper_model.transcribe(audio_path)
    return result["text"]

# TTS 함수
def text_to_speech(text, filename='response.mp3'):
    tts = gTTS(text=text, lang='ko')
    tts.save(filename)
    return filename

# GPT-4 함수
def generate_gpt4_response(prompt):
    response = openai.Completion.create(
        model="text-davinci-004",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].text.strip()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    audio_path = data.get('audio_path')
    
    # STT
    user_input = speech_to_text(audio_path)
    
    # KIWI 엔진 처리 (필요한 전처리 또는 키워드 추출)
    kiwi_tokens = kiwi.tokenize(user_input)
    keywords = [token.form for token in kiwi_tokens if token.tag in ['NNG', 'NNP', 'VV', 'VA']]
    
    # GPT-4 응답 생성
    gpt4_response = generate_gpt4_response(user_input)
    
    # TTS
    tts_path = text_to_speech(gpt4_response)
    
    response = {
        "user_input": user_input,
        "gpt4_response": gpt4_response,
        "tts_path": tts_path
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
