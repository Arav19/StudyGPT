from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Import CORS for cross-origin requests
import openai
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Retrieve your OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_input = data.get("message", "")

        # Send the message to OpenAI's ChatCompletion API and get a response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )

        reply_text = response['choices'][0]['message']['content'].strip()
        return jsonify({"response": reply_text})

    except openai.error.OpenAIError as e:
        print("OpenAI API Error:", e)
        return jsonify({"response": "An error occurred with the OpenAI API."}), 500
    except Exception as e:
        print("General Error:", e)
        return jsonify({"response": "An unexpected error occurred."}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

