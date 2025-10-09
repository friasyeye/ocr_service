import os
from flask import Flask, request, jsonify
from paddleocr import PaddleOCR
from pdf2image import convert_from_path

app = Flask(__name__)

ocr = None  # Lazy initialization

@app.route("/")
def healthcheck():
    return jsonify({"status": "ok", "message": "OCR service running"})

@app.route("/ocr", methods=["POST"])
def run_ocr():
    global ocr
    if ocr is None:
        ocr = PaddleOCR(use_angle_cls=True, lang="en")  # descarga modelos la primera vez

    file = request.files['file']
    filename = file.filename.lower()
    temp_path = "/tmp/uploaded"

    if filename.endswith(".pdf"):
        pdf_path = f"{temp_path}.pdf"
        file.save(pdf_path)
        images = convert_from_path(pdf_path)
        results = []
        for i, img in enumerate(images):
            img_path = f"{temp_path}_{i}.png"
            img.save(img_path, "PNG")
            result = ocr.ocr(img_path, cls=True)
            results.append({"page": i + 1, "result": result})
        return jsonify(results)

    else:  # imagen normal
        img_path = f"{temp_path}.png"
        file.save(img_path)
        result = ocr.ocr(img_path, cls=True)
        return jsonify(result)

if __name__ == "__main__":
    # Usar el puerto definido por la plataforma (Easypanel), o 80 por defecto
    port = int(os.environ.get("PORT", 80))
    app.run(host="0.0.0.0", port=port)
