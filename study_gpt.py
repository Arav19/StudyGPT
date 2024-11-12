from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Import CORS for cross-origin requests
import openai
import os
import logging

# Import only available error classes from OpenAI library
from openai.error import APIConnectionError, AuthenticationError, RateLimitError, OpenAIError

app = Flask(__name__)
CORS(app)  # Enable CORS

# Set up basic logging
logging.basicConfig(level=logging.INFO)

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

        # Log user input
        logging.info(f"User input: {user_input}")

        # Send the message to OpenAI ChatCompletion API and get a response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )

        # Log the response to see if there are any issues
        logging.info(f"OpenAI Response: {response}")

        reply_text = response.choices[0].message['content'].strip()
        return jsonify({"response": reply_text})

    except APIConnectionError as e:  # Correct for network issues
        logging.error(f"API Connection Error: {e}")
        return jsonify({"response": "A network error occurred."}), 500
    except AuthenticationError as e:  # Authentication issues
        logging.error(f"Authentication Error: {e}")
        return jsonify({"response": "API Key authentication failed."}), 401
    except RateLimitError as e:  # Rate limit errors
        logging.error(f"Rate Limit Exceeded: {e}")
        return jsonify({"response": "Rate limit exceeded, please try again later."}), 429
    except OpenAIError as e:  # Generic OpenAI API errors
        logging.error(f"OpenAI API Error: {e}")
        return jsonify({"response": "An error occurred with the OpenAI API."}), 500
    except Exception as e:
        logging.error(f"General Error: {e}")
        return jsonify({"response": "An unexpected error occurred."}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
