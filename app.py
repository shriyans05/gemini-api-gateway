from flask import Flask, request, jsonify
from google import genai
from google.genai import types
import os
import tempfile

app = Flask(__name__)

MY_SERVER_SECRET = os.environ.get("MY_SERVER_SECRET")
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/generate', methods=['POST'])
def generate_response():
    # 1. The Security Bouncer
    provided_key = request.headers.get('X-API-Key')
    if not provided_key or provided_key != MY_SERVER_SECRET:
        return jsonify({"error": "Unauthorized."}), 401

    try:
        # 2. Handle Text-Only Requests (Like Career Compass)
        if request.is_json:
            data = request.json
            user_prompt = data.get('prompt')
            system_instruction = data.get('system_instruction', "You are a helpful assistant.")
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_prompt,
                config=genai.types.GenerateContentConfig(system_instruction=system_instruction)
            )
            return jsonify({"response": response.text}), 200

        # 3. Handle Audio/File Requests (Like KSP Smart FIR)
        else:
            user_prompt = request.form.get('prompt', '')
            system_instruction = request.form.get('system_instruction', "You are a helpful assistant.")
            
            if 'file' not in request.files:
                return jsonify({"error": "No file provided."}), 400
                
            file = request.files['file']
            
            # Save audio locally
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                file.save(temp_audio.name)
                temp_path = temp_audio.name
            
            try:
                # Upload to Google's servers
                uploaded_file = client.files.upload(path=temp_path)
                
                # STRICT FORMATTING: Force the SDK to recognize this as a remote File URI
                audio_part = types.Part.from_uri(
                    file_uri=uploaded_file.uri,
                    mime_type=uploaded_file.mime_type
                )
                
                # Ask Gemini to process both the prompt and the explicitly formatted audio part
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[user_prompt, audio_part],
                    config=types.GenerateContentConfig(system_instruction=system_instruction)
                )
                
                # Delete the file from Google's servers to save space
                client.files.delete(name=uploaded_file.name)
                
                return jsonify({"response": response.text}), 200
            finally:
                # Delete the local temp file
                if os.path.exists(temp_path):
                    os.remove(temp_path)

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)