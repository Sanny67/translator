from flask import Flask, render_template, request, jsonify
from googletrans import Translator, LANGUAGES

app = Flask(__name__)
translator = Translator()

available_languages = [{"code": code, "name": name[:1].upper() + name[1:]} for code, name in LANGUAGES.items()]

@app.route('/')
def home():
    return render_template("index.html", languages=available_languages)

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get("text", "")
    target_lang = data.get("target_lang", "en")

    if not text.strip():
        return jsonify({"translated_text": ""})

    detected_lang = translator.detect(text).lang  # Auto-detect language
    translated = translator.translate(text, src=detected_lang, dest=target_lang)
    
    return jsonify({"translated_text": translated.text, "detected_lang": detected_lang})

if __name__ == '__main__':
    app.run(debug=True)
