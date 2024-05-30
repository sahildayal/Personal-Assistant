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

def main():
    print("Welcome to your personal assistant! Type 'exit' to end the conversation.")
    while True:
        question = input("You: ")
        if question.lower() == 'exit':
            print("Goodbye!")
            break
        answer = ask_openai(question)
        print(f"Assistant: {answer}")

if __name__ == "__main__":
    main()
