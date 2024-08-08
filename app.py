import os
from flask import Flask, request, send_file, render_template, jsonify
import cv2
import pytesseract
import pdf2image
import numpy as np
import json

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image):
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, binary_image = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary_image

def process_pdf(pdf_path):
    images = pdf2image.convert_from_path(pdf_path)
    return [np.array(img) for img in images]

def process_file(file_path):
    if file_path.lower().endswith('.pdf'):
        images = process_pdf(file_path)
    else:
        images = [cv2.imread(file_path)]
    
    all_text = []
    total_images = len(images)
    
    for i, image in enumerate(images):
        processed_image = preprocess_image(image)
        custom_config = r'--oem 3 --psm 6 -l jpn'
        text = pytesseract.image_to_string(processed_image, config=custom_config)
        all_text.append(text)
        progress = (i + 1) / total_images * 100
        yield f"data: {json.dumps({'progress': progress})}\n\n"
    
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], 'output.txt')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(all_text))
    
    yield f"data: {json.dumps({'progress': 100, 'complete': True})}\n\n"

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        if file and allowed_file(file.filename):
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return jsonify({'success': True, 'filename': filename})
    return render_template('upload.html')

@app.route('/process/<filename>')
def process(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return app.response_class(process_file(file_path), mimetype='text/event-stream')

@app.route('/download')
def download():
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], 'output.txt')
    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    app.run(debug=True)