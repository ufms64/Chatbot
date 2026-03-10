from groq import Groq

client = Groq(api_key="")  

def chat_with_ai(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  
        messages=[
            {"role": "system", "content": "You are a friendly chatbot."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    # Extract text safely
    return response.choices[0].message.content

print("buddy!! I am ready✌️! Type exit/quit/bye to stop.")

while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Chatbot: Goodbye!")
        break

    try:
        reply = chat_with_ai(user_input)
        print("Chatbot:", reply)
    except Exception as e:
        print("Error:", e)