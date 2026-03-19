from flask import Flask, request, jsonify
from google import genai
import os

app = Flask(__name__)

MY_SERVER_SECRET = os.environ.get("MY_SERVER_SECRET")
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/generate', methods=['POST'])
def generate_response():
    provided_key = request.headers.get('X-API-Key')
    if not provided_key or provided_key != MY_SERVER_SECRET:
        return jsonify({"error": "Unauthorized."}), 401

    data = request.json
    user_prompt = data.get('prompt')
    system_instruction = data.get('system_instruction', "You are a helpful assistant.")

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_prompt,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_instruction,
            )
        )
        return jsonify({"response": response.text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)