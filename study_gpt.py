from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Import CORS for cross-origin requests
import openai
import os
import logging

# Import available error classes from OpenAI library
from openai.error import APIConnectionError, AuthenticationError, RateLimitError, OpenAIError

app = Flask(__name__)
CORS(app)  # Enable CORS

# Set up detailed logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Retrieve your OpenAI API key from the environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key:
    logging.info("OpenAI API key loaded successfully.")
else:
    logging.error("OpenAI API key not found. Make sure it is set in the environment variables.")

openai.api_key = openai_api_key

@app.route('/')
def home():
    logging.info("Home page accessed.")
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        if not data or "message" not in data:
            logging.warning("No message found in request data.")
            return jsonify({"response": "No message provided."}), 400

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

        # Extract the response text
        reply_text = response['choices'][0]['message']['content'].strip()
        logging.info(f"Reply text: {reply_text}")
        return jsonify({"response": reply_text})

    except APIConnectionError as e:
        logging.error(f"API Connection Error: {e}")
        return jsonify({"response": "A network error occurred."}), 500
    except AuthenticationError as e:
        logging.error(f"Authentication Error: {e}")
        return jsonify({"response": "API Key authentication failed."}), 401
    except RateLimitError as e:
        logging.error(f"Rate Limit Exceeded: {e}")
        return jsonify({"response": "Rate limit exceeded, please try again later."}), 429
    except OpenAIError as e:
        logging.error(f"OpenAI API Error: {e}")
        return jsonify({"response": "An error occurred with the OpenAI API."}), 500
    except Exception as e:
        logging.error(f"General Error: {e}")
        return jsonify({"response": "An unexpected error occurred."}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logging.info(f"Starting Flask server on port {port}.")
    app.run(debug=True, host='0.0.0.0', port=port)
