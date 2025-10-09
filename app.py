from flask import Flask, request, jsonify
from paddleocr import PaddleOCR

app = Flask(__name__)

# Inicializamos OCR en modo lazy (solo una vez al primer request)
ocr = None

@app.route("/")
def healthcheck():
    return jsonify({"status": "ok", "message": "OCR service running"})

@app.route("/ocr", methods=["POST"])
def run_ocr():
    global ocr
    if ocr is None:
        # Inicializa aquí la primera vez que se usa
        ocr = PaddleOCR(use_angle_cls=True, lang="en")
    file = request.files['file']
    image_path = "/tmp/uploaded.png"
    file.save(image_path)

    result = ocr.ocr(image_path, cls=True)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

