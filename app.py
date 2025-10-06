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
        # Recibir imagen en base64
        data = request.get_json()
        image_base64 = data.get("image_base64")

        if not image_base64:
            return jsonify({"error": "No image_base64 provided"}), 400

        # Convertir de base64 a imagen
        image_data = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_data))

        # Ejecutar OCR con Tesseract
        text = pytesseract.image_to_string(image, lang="spa")  # español

        return jsonify({"text": text.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
