from flask import Flask, render_template, request, jsonify
import requests
import os

# Initialize Flask app
app = Flask(__name__)

# Constants
CHUNK_SIZE = 1024
VOICE_ID = "cgSgspJ2msm6clMCkdW9"  # Replace with your voice ID
XI_API_KEY = "sk_0b661596b9b88c35982e5d395de1c48a34126674db564e6c"  # Replace with your API key
OUTPUT_DIR = "output_audio_files"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Home route to serve the frontend
@app.route("/")
def index():
    return render_template("index.html")

# API route for generating audio
@app.route("/generate-audio", methods=["POST"])
def generate_audio():
    data = request.json
    print("---------------------------")
    print("---------------------------")
    print(data)
    print("---------------------------")
    text_to_speak = data.get("text")
    file_name = data.get("fileName", "output").replace(" ", "_") + ".mp3"
    VOICE_ID=data.get("voice_id")
    print(VOICE_ID)

    tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"
    headers = {
        "Accept": "application/json",
        "xi-api-key": XI_API_KEY
    }
    payload = {
        "text": text_to_speak,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.0,
            "use_speaker_boost": True
        }
    }

    response = requests.post(tts_url, headers=headers, json=payload, stream=True)
    if response.ok:
        output_path = os.path.join(OUTPUT_DIR, file_name)
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                f.write(chunk)
        return jsonify({"success": True, "message": f"Audio saved as {file_name}"})
    else:
        return jsonify({"success": False, "error": response.text}), 400

if __name__ == "__main__":
    app.run(debug=True)
