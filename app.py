from flask import Flask, request, jsonify
from paddleocr import PaddleOCR
from PIL import Image
import io, base64
import numpy as np
from pdf2image import convert_from_bytes

app = Flask(__name__)

# Inicializamos PaddleOCR con español (también reconoce catalán decentemente)
ocr = PaddleOCR(use_angle_cls=True, lang='es')

@app.route('/')
def index():
    return jsonify({"message": "OCR service running with PaddleOCR", "status": "ok"})

@app.route('/ocr', methods=['POST'])
def ocr_endpoint():
    try:
        # Caso 1: archivo enviado como multipart/form-data
        if 'file' in request.files:
            file = request.files['file']
            filename = file.filename.lower()

            if filename.endswith('.pdf'):
                # Convertir PDF escaneado en imágenes (todas las páginas)
                images = convert_from_bytes(file.read())
                texts = []
                for img in images:
                    results = ocr.ocr(np.array(img), cls=True)
                    for line in results[0]:
                        texts.append(line[1][0])
                return jsonify({"text": "\n".join(texts)})

            else:
                # Imagen (jpg, png…)
                image = Image.open(file.stream).convert('RGB')
                results = ocr.ocr(np.array(image), cls=True)
                texts = [line[1][0] for line in results[0]]
                return jsonify({"text": "\n".join(texts)})

        # Caso 2: JSON con base64
        data = request.get_json(silent=True)
        if data and "image_base64" in data:
            image_base64 = data["image_base64"]
            image_data = base64.b64decode(image_base64)
            image = Image.open(io.BytesIO(image_data)).convert('RGB')
            results = ocr.ocr(np.array(image), cls=True)
            texts = [line[1][0] for line in results[0]]
            return jsonify({"text": "\n".join(texts)})

        return jsonify({"error": "No file or image_base64 provided"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
