from flask import Flask, request, render_template_string, jsonify, send_file
import openai
import speech_recognition as sr
from gtts import gTTS
import os
import io

openai.api_key = ''

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Magnus - Your Personal Assistant</title>
    <style>
        body { 
            font-family: inherit; 
            margin: 0; 
            padding: 0; 
            background: url('/static/bg.png') no-repeat center center fixed; 
            background-size: cover;
            color: #333;
        }
        .container {
            max-width: 600px; 
            margin: 100px auto; 
            padding: 20px; 
            background: rgba(255, 255, 255, 0.8); 
            border-radius: 10px; 
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #4CAF50; 
            text-align: center;
        }
        form {
            display: flex; 
            justify-content: center; 
            margin-bottom: 20px;
        }
        input[type=text] {
            width: 70%; 
            padding: 10px; 
            border: 1px solid #ccc; 
            border-radius: 5px;
        }
        input[type=submit] {
            padding: 10px 20px; 
            border: none; 
            background-color: #4CAF50; 
            color: white; 
            border-radius: 5px; 
            cursor: pointer;
            margin-left: 10px;
        }
        .chat-box {
            margin-top: 20px; 
            padding: 10px; 
            background: #f9f9f9; 
            border-radius: 5px;
        }
        .user { color: blue; }
        .assistant { color: green; }
        .audio-button {
            padding: 10px 20px;
            border: none;
            background-color: #f39c12;
            color: white;
            border-radius: 5px;
            cursor: pointer;
        }
    </style>
    <script>
        function startRecognition() {
            fetch('/start_recognition')
            .then(response => response.json())
            .then(data => {
                document.getElementById('question').value = data.question;
                document.getElementById('askForm').submit();
            });
        }

        function playAudio() {
            fetch('/get_audio')
            .then(response => response.blob())
            .then(blob => {
                const url = URL.createObjectURL(blob);
                const audio = new Audio(url);
                audio.play();
            });
        }
    </script>
</head>
<body>
    <div class="container">
        <h1>Welcome Sahil!</h1>
        <form id="askForm" method="post" action="/" enctype="multipart/form-data">
            <input id="question" type="text" name="question" placeholder="Ask me anything bro..." required>
            <input type="submit" value="Ask">
        </form>
        <button class="audio-button" onclick="startRecognition()">Ask by Voice</button>
        <div class="chat-box">
            {% if question and answer %}
                <p class="user"><strong>You:</strong> {{ question }}</p>
                <p class="assistant"><strong>Magnus:</strong> {{ answer }}</p>
                <script>
                    playAudio();
                </script>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

def ask_openai(question):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=question,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )
    answer = response.choices[0].text.strip()
    return answer

@app.route("/", methods=["GET", "POST"])
def index():
    question = None
    answer = None
    if request.method == "POST":
        question = request.form["question"]
        answer = ask_openai(question)
        tts = gTTS(answer)
        audio_stream = io.BytesIO()
        tts.write_to_fp(audio_stream)
        audio_stream.seek(0)
        global last_audio_stream
        last_audio_stream = audio_stream
    return render_template_string(html_template, question=question, answer=answer)

@app.route("/start_recognition", methods=["GET"])
def start_recognition():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        question = recognizer.recognize_google(audio)
        print("You said: " + question)
    except sr.UnknownValueError:
        question = "Sorry, I did not understand that."
    except sr.RequestError:
        question = "Sorry, the service is down."

    return jsonify({'question': question})

@app.route("/get_audio", methods=["GET"])
def get_audio():
    global last_audio_stream
    return send_file(last_audio_stream, mimetype='audio/mp3')

if __name__ == "__main__":
    last_audio_stream = None
    if not os.path.exists("static"):
        os.makedirs("static")
    app.run(debug=True)
