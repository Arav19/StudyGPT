from flask import Flask, request, jsonify, render_template
import openai
import os

app = Flask(__name__)

# Retrieve your OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure this is set in Render's environment

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_input = data.get("message", "")  # Capture the user message from the frontend
        
        # Send the message to OpenAI's ChatCompletion API and get a response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use the desired model
            messages=[{"role": "user", "content": user_input}]
        )
        
        # Extract and return the response content
        reply_text = response['choices'][0]['message']['content'].strip()
        return jsonify({"response": reply_text})

    except openai.error.OpenAIError as e:
        print("OpenAI API Error:", e)
        return jsonify({"response": "An error occurred with the OpenAI API."}), 500

    except Exception as e:
        print("General Error:", e)
        return jsonify({"response": "An unexpected error occurred."}), 500

if __name__ == '__main__':
    # Ensure the app uses the correct port assigned by Render
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)



