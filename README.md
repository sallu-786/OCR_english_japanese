PDF and Image OCR Processing Application
=========================================

The application provides a web interface to upload PDF and image files, processes these files to extract text using OCR, and allows users to download the extracted text as a .txt file.
 For PDFs, it uses `pdf2image` to convert each page to an image.
- For image files, it uses OpenCV to read the image.
- The `preprocess_image` function converts images to grayscale, applies Gaussian blur, and performs binary thresholding to prepare the image for OCR.
- The processed image is passed to `pytesseract` for text extraction with custom configurations optimized for Japanese (`--oem 3 --psm 6 -l jpn`). 
- The extracted text is written to `output/output.txt`.




Setup Environment
-----------------
1. Clone this repository:

    git clone https://github.com/yourusername/ocr-processing-app.git


   cd ocr-processing-app

3. Create a virtual environment:

   In windows use the following commands to create and activate virtual environment:

   
    python -m venv my_venv

    my_venv\Scripts\activate


1. Install the required packages:


   pip install -r requirements.txt

2. Install Tesseract OCR:


Download the Tesseract [installer from https://github.com/UB-Mannheim/tesseract/wiki.](https://github.com/tesseract-ocr/tesseract)

Remember to add Tesseract to your system PATH. Also for Japanese you must add jpn.traineddata in C:\Program Files\Tesseract-OCR\tessdata 

3. Install Poppler (for pdf2image):
   
Download the Poppler installer from http://blog.alivate.com.au/poppler-windows/.
Also Add Poppler to your system PATH.

Application Overview
--------------------
The application provides a web interface to upload PDF and image files, processes these files to extract text using OCR, and allows users to download the extracted text as a .txt file.
 For PDFs, it uses `pdf2image` to convert each page to an image.
- For image files, it uses OpenCV to read the image.
- The `preprocess_image` function converts images to grayscale, applies Gaussian blur, and performs binary thresholding to prepare the image for OCR.
- The processed image is passed to `pytesseract` for text extraction with custom configurations optimized for Japanese (`--oem 3 --psm 6 -l jpn`). 
- The extracted text is written to `output/output.txt`.


Running the Application
-----------------------
1. Start the Flask application:
    python app.py

2. Access the application:
    - Open your web browser and go to `http://127.0.0.1:5000`.


