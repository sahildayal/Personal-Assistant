#personal assistant
import openai

openai.api_key = ''

def ask_openai(question):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",  # Use the appropriate engine
        prompt=question,
        max_tokens=150,  
        n=1,
        stop=None,
        temperature=0.5,
    )

    answer = response.choices[0].text.strip()
    return answer
