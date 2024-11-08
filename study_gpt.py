
from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)

# Retrieve your OpenAI API key from the environment variable
openai.api_key = os.getenv("")  # Ensure you've set this in your environment

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']  # This captures the user message from the frontend
    try:
        # Send the message to OpenAI and get a response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        reply_text = response['choices'][0]['message']['content'].strip()
        return jsonify({"response": reply_text})  # Send the reply back to the webpage
    except openai.error.OpenAIError as e:
        print("An error occurred with the OpenAI API:", e)
        return jsonify({"response": "An error occurred with the OpenAI API."})
    except Exception as e:
        print("A general error occurred:", e)
        return jsonify({"response": "An unexpected error occurred."})

if __name__ == '__main__':
    app.run(debug=True, port=8000)



