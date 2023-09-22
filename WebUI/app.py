import time
import fitz  # pip install PyMuPDF, not fitz
import json

from flask import *
from werkzeug.utils import secure_filename
from opencc import OpenCC

from ocr import *
from export import *
from function import *

app = Flask(__name__)

# file storage
UPLOAD_FOLDER_IMG = 'uploadimg'
UPLOAD_FOLDER_PDF = 'uploadpdf'
VISUALIZATION = 'static'
ALLOWED_EXTENSIONS_IMG = {'png', 'jpg', 'jpeg'}
ALLOWED_EXTENSIONS_PDF = {'pdf'}

REVERSE_TOGGLE = False

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_IMG
app.config['UPLOAD_FOLDER_2'] = UPLOAD_FOLDER_PDF
app.config['VISUALIZATION'] = VISUALIZATION

# 500MB limit for single uploadimg
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024
app.secret_key = "NCU_MIAT_LAB"


# verify file extensions
def allowed_file_img(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS_IMG


def allowed_file_pdf(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS_PDF


@app.route('/')
def index():
    file_cleanup("uploadimg")
    file_cleanup("uploadpdf")
    file_cleanup("static")

    return render_template('index.html', template_folder='./')


@app.route('/chinesevertical', methods=['GET', 'POST'])
def chinese_vertical():
    global REVERSE_TOGGLE

    if request.method == 'POST':
        conditional_flag = request.form
        # print(conditional_flag['conditionalFlag'])

        if int(conditional_flag['conditionalFlag']) == 1:
            REVERSE_TOGGLE = True
        else:
            REVERSE_TOGGLE = False

    # print(CHINESE_VERTICAL_TOGGLE)

    return render_template('index.html')


@app.route('/uploadimg', methods=['GET', 'POST'])
def upload_file():
    global REVERSE_TOGGLE

    cc = OpenCC('s2twp')

    if request.method == 'POST':
        uploaded_files = request.files.getlist("file1[]")
        list_result = []
        ocr_final_result = str("")
        counter = 1
        total_images = len(uploaded_files)

    for file in uploaded_files:
        if file and allowed_file_img(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            return redirect(url_for("index"))

        ocr_result = image_ocr_match(os.path.join(app.config['UPLOAD_FOLDER'], filename), counter)

        # chinese vertical written form
        if REVERSE_TOGGLE:
            ocr_result = written_reverse(ocr_result)
        else:
            ocr_result = written_default(ocr_result)

        for r in ocr_result:
            s2t = cc.convert(str(r[1][0]))
            list_result.append(s2t)
            ocr_final_result = ocr_final_result + str(s2t)

        progress_bar_calculation(counter, total_images)

        counter += 1

    ocr_final_result = remove_special_characters(ocr_final_result)

    ocr_json = json.dumps(
        dict(text=ocr_final_result),
        ensure_ascii=False)

    txt_export_web(ocr_final_result)
    json_export_web(ocr_json)

    return render_template('result.html',
                           ocr_final_result=ocr_final_result,
                           carousel_index=total_images)


@app.route('/uploadpdf', methods=['GET', 'POST'])
def upload_file_2():
    global REVERSE_TOGGLE

    cc = OpenCC('s2twp')

    if request.method == 'POST':
        uploaded_files = request.files.getlist("file2[]")
        list_result = []
        ocr_final_result = str()

    for file in uploaded_files:
        if file and allowed_file_pdf(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER_2'], filename))
        else:
            return redirect(url_for("index"))

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

            pix.save(os.path.join(app.config['UPLOAD_FOLDER'], 'P' + str(pg + 1) + '.png'))

            ocr_result = image_ocr_match(os.path.join(app.config['UPLOAD_FOLDER'], 'P' + str(pg + 1) + '.png'), pg + 1)

            progress_bar_calculation(pg + 1, page_number)

            # chinese vertical written form
            if REVERSE_TOGGLE:
                ocr_result = written_reverse(ocr_result)
            else:
                ocr_result = written_default(ocr_result)

            for r in ocr_result:
                s2t = cc.convert(str(r[1][0]))
                list_result.append(s2t)
                ocr_final_result = ocr_final_result + str(s2t)

    ocr_final_result = remove_special_characters(ocr_final_result)

    ocr_json = json.dumps(
        dict(text=ocr_final_result),
        ensure_ascii=False)

    txt_export_web(ocr_final_result)
    json_export_web(ocr_json)

    return render_template('result.html',
                           ocr_final_result=ocr_final_result,
                           carousel_index=page_number)


@app.route('/downloadtxt')
def download_txt():
    return send_file(
        'download/output.txt',
        mimetype='text/plain',
        download_name='result.txt',
        as_attachment=True)


@app.route('/downloadjson')
def download_json():
    return send_file(
        'download/output.json',
        mimetype='application/json',
        download_name='result.json',
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
    app.run(host="0.0.0.0", port=9487)
