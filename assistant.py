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
    <title>Personal Assistant</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        input[type=text] { width: 300px; padding: 10px; }
        input[type=submit] { padding: 10px; }
        .chat-box { margin-top: 20px; }
        .user { color: blue; }
        .assistant { color: green; }
    </style>
</head>
<body>
    <h1>Welcome to your personal assistant!</h1>
    <form method="post" action="/">
        <input type="text" name="question" placeholder="Ask me anything..." required>
        <input type="submit" value="Ask">
    </form>
    <div class="chat-box">
        {% if question and answer %}
            <p class="user"><strong>You:</strong> {{ question }}</p>
            <p class="assistant"><strong>Assistant:</strong> {{ answer }}</p>
        {% endif %}
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
