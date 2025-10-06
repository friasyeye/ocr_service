from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import io
import fitz  # PyMuPDF

app = Flask(__name__)

@app.route('/ocr', methods=['POST'])
def ocr_endpoint():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    # Si el archivo es PDF, convertimos la primera página a imagen
    if file.filename.lower().endswith('.pdf'):
        pdf_bytes = file.read()
        pdf_doc = fitz.open(stream=pdf_bytes, filetype='pdf')
        page = pdf_doc.load_page(0)
        pix = page.get_pixmap()
        image = Image.open(io.BytesIO(pix.tobytes("png")))
    else:
        image = Image.open(file.stream)

    text = pytesseract.image_to_string(image, lang='spa+cat')
    return jsonify({'text': text})
    
@app.route('/')
def root():
    return jsonify({'status': 'ok', 'message': 'OCR service running'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
