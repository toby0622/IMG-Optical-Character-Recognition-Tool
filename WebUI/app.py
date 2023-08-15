import time
import fitz # pip install PyMuPDF

from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import send_file
from flask import Response
from flask import stream_with_context
from werkzeug.utils import secure_filename
from opencc import OpenCC

from ocr import *
from export import *
from function import *


app = Flask(__name__)

# file storage
UPLOAD_FOLDER_IMG = 'uploadimg'
UPLOAD_FOLDER_PDF = 'uploadpdf'
ALLOWED_EXTENSIONS_IMG = {'png', 'jpg', 'jpeg'}
ALLOWED_EXTENSIONS_PDF = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_IMG
app.config['UPLOAD_FOLDER_2'] = UPLOAD_FOLDER_PDF
# 500MB limit for single uploadimg
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024

progress_bar_ratio = 0


# verify file extensions
def allowed_file_img(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS_IMG


def allowed_file_pdf(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS_PDF


# dynamic progress bar
def progress_bar_calculation(current_images, total_images):
    global progress_bar_ratio
    progress_bar_ratio = current_images / float(total_images)
    progress_bar_ratio = int(round(progress_bar_ratio, 2) * 100)


# value getter for JavaScript
def get_bar_ratio():
    global progress_bar_ratio
    return progress_bar_ratio


@app.route('/')
def index():
    return render_template('index.html', template_folder='./')


@app.route('/uploadimg', methods=['GET', 'POST'])
def upload_file():
    cc = OpenCC('s2tw')

    if request.method == 'POST':
        uploaded_files = request.files.getlist("file1[]")
        filenames = []
        ocr_results = []
        ocr_list_result = []
        ocr_final_result = str()
        counter = 1
        total_images = len(uploaded_files)

    for file in uploaded_files:
        if file and allowed_file_img(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filenames.append(filename)

        ocr_result = image_ocr_match(os.path.join(app.config['UPLOAD_FOLDER'], filename), counter)

        for r in ocr_result:
            ocr_results.append(r)

        # sorting using recognition box x-axis, from right to left
        ocr_results = sorted(ocr_results, key=lambda x: (x[0][1][0]), reverse=True)

        for o in ocr_results:
            cc.convert(str(o))
            ocr_list_result.append(o[1][0])

        ocr_results.clear()

        progress_bar_calculation(counter, total_images)

        counter += 1

    for f in ocr_list_result:
        ocr_final_result = ocr_final_result + str(f)

    txt_export_web(ocr_final_result)

    return render_template('result.html',
                           filenames=filenames,
                           ocr_final_result=ocr_final_result)


@app.route('/uploadpdf', methods=['GET', 'POST'])
def upload_file_2():
    cc = OpenCC('s2tw')

    if request.method == 'POST':
        uploaded_files = request.files.getlist("file2[]")
        filenames = []
        ocr_results = []
        ocr_list_result = []
        ocr_final_result = str()
        counter = 1
        total_pdf = len(uploaded_files)

    for file in uploaded_files:
        if file and allowed_file_pdf(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER_2'], filename))
            filenames.append(filename)

        pdf_doc = fitz.open(os.path.join(app.config['UPLOAD_FOLDER_2'], filename))
        page_number = pdf_doc.page_count

        for pg in range(0, page_number):
            page = pdf_doc[pg]
            rotate = int(0)  # no rotation
            # default A4 portrait = 595 x 842
            zoom_x = 8  # horizontal
            zoom_y = 8  # vertical
            mat = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
            pix = page.get_pixmap(matrix=mat, alpha=False)

            pix.save(os.path.join(app.config['UPLOAD_FOLDER'], 'P' + str(pg) + '.png'))

            ocr_result = image_ocr_match(os.path.join(app.config['UPLOAD_FOLDER'], 'P' + str(pg) + '.png'), pg)

            for r in ocr_result:
                ocr_results.append(r)

        for o in ocr_results:
            cc.convert(str(o))
            ocr_list_result.append(o[1][0])

        ocr_results.clear()

        progress_bar_calculation(counter, total_pdf)

        counter += 1

    for f in ocr_list_result:
        ocr_final_result = ocr_final_result + str(f)

    txt_export_web(ocr_final_result)

    return render_template('result.html',
                           filenames=filenames,
                           ocr_final_result=ocr_final_result)


@app.route('/uploadimg/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/uploadpdf/<filename>')
def uploaded_file_2(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER_2'], filename)


@app.route('/download')
def download_txt():
    return send_file(
        'download/output.txt',
        mimetype='text/plain',
        download_name='result.txt',
        as_attachment=True)


@app.route('/progress')
def progress():
    @stream_with_context
    def generate():
        ratio = get_bar_ratio()

        while ratio < 100:
            yield "data:" + str(ratio) + "\n\n"
            # print("ratio:", ratio)
            ratio = get_bar_ratio()

            time.sleep(1)

    return Response(generate(), mimetype='text/event-stream')


if __name__ == "__main__":
    file_cleanup("uploadimg")
    file_cleanup("uploadpdf")

    app.run(debug=True, port=8000)
