from flask import Flask, request, jsonify
from paddleocr import PaddleOCR
import os

app = Flask(__name__)

# Inicializar OCR (en español por defecto)
ocr = PaddleOCR(use_angle_cls=True, lang='es')

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok", "message": "OCR service is running"})

@app.route("/ocr", methods=["POST"])
def run_ocr():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    filepath = os.path.join("/tmp", file.filename)
    file.save(filepath)

    result = ocr.ocr(filepath, cls=True)

    text = []
    for line in result[0]:
        text.append(line[1][0])

    return jsonify({"text": text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
