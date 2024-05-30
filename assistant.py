from flask import Flask, request, render_template_string
import openai

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
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome Sahil!</h1>
        <form method="post" action="/">
            <input type="text" name="question" placeholder="Ask me anything broo..." required>
            <input type="submit" value="Ask">
        </form>
        <div class="chat-box">
            {% if question and answer %}
                <p class="user"><strong>You:</strong> {{ question }}</p>
                <p class="assistant"><strong>Magnus:</strong> {{ answer }}</p>
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
    return render_template_string(html_template, question=question, answer=answer)

if __name__ == "__main__":
    app.run(debug=True)
