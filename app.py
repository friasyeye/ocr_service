from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "OCR service running", "status": "ok"})

@app.route('/ocr', methods=['POST'])
def ocr():
    try:
        # Caso 1: Imagen enviada como archivo (multipart/form-data)
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({"error": "No selected file"}), 400

            image = Image.open(file.stream)

        else:
            # Caso 2: Imagen enviada en JSON como base64
            data = request.get_json(silent=True)
            if not data or 'image_base64' not in data:
                return jsonify({"error": "No image provided"}), 400

            image_base64 = data['image_base64']
            image_data = base64.b64decode(image_base64)
            image = Image.open(io.BytesIO(image_data))

        # Ejecutar OCR con Tesseract
        text = pytesseract.image_to_string(image, lang="spa")  # español

        return jsonify({"text": text.strip()})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
