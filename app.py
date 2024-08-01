from flask import Flask, request, jsonify
import openai
import logging
import requests

app = Flask(__name__)

# إعداد مفتاح API الخاص بـ OpenAI
openai.api_key = "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"

# إعداد مفتاح API الخاص بـ DeepAI
deepai_api_key = '76f97ccf-8b48-4fad-b318-1d39ac9a8dc2'

def analyze_video(video_url):
    response = requests.post(
        "https://api.deepai.org/api/video-recognition",
        data={
            'video': video_url,
        },
        headers={'api-key': deepai_api_key}
    )
    return response.json()

@app.route("/chat", methods=['POST'])
def chat():
    try:
        if request.content_type != 'application/json':
            return jsonify({"response": "Unsupported Media Type: Content-Type must be application/json"}), 415

        incoming_msg = request.json.get('message', '').strip()
        app.logger.debug(f"Received message: {incoming_msg}")

        if not incoming_msg:
            return jsonify({"response": "The message is empty. Please provide a valid message."}), 400

        # تحليل الفيديو باستخدام DeepAI
        video_url = 'https://drive.google.com/file/d/1EchjT9VV8WqAO4Zi7kUbi6WUf02Wwm-c/view?usp=drive_link'  # استبدل برابط الفيديو الخاص بك
        analysis_result = analyze_video(video_url)
        app.logger.debug(f"Analysis result: {analysis_result}")

        # معالجة النتائج وإعداد الرد
        labels = analysis_result.get('output', [])
        if labels:
            answer = "The video contains: " + ", ".join(labels)
        else:
            answer = "No recognizable objects found in the video."

        app.logger.debug(f"Sending response: {answer}")
        return jsonify({"response": answer})
    except Exception as e:
        app.logger.error(f"Error: {str(e)}", exc_info=True)
        return jsonify({"response": "Sorry, an error occurred. Please try again later."}), 500

if __name__ == "__main__":
    app.run(debug=True)
