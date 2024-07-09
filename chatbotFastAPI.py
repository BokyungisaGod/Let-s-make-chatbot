from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
MODEL = "gpt-4o"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

html_form = """
<!DOCTYPE html>
<html>
<head>
    <title>ChatGPT with FastAPI</title>
</head>
<body>
    <h1>ChatGPT with FastAPI</h1>
    <form method="post">
        <label for="user_message">User:</label>
        <input type="text" id="user_message" name="user_message">
        <input type="submit" value="Send">
    </form>
    <div id="chatbox">
    {messages}
    </div>
</body>
</html>
"""

messages = []

@app.get("/", response_class=HTMLResponse)
async def get_form():
    formatted_messages = ""
    for message in messages:
        role = "User" if message['role'] == 'user' else "Assistant"
        formatted_messages += f"<p><strong>{role}:</strong> {message['content']}</p>"
    return html_form.format(messages=formatted_messages)

@app.post("/", response_class=HTMLResponse)
async def handle_form(user_message: str = Form(...)):
    global messages
    messages.append({"role": "user", "content": user_message})

    completion = client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )
    response = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": response})

    formatted_messages = ""
    for message in messages:
        role = "User" if message['role'] == 'user' else "Assistant"
        formatted_messages += f"<p><strong>{role}:</strong> {message['content']}</p>"
    return html_form.format(messages=formatted_messages)
