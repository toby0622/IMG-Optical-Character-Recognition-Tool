from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import send_file
from werkzeug.utils import secure_filename
from opencc import OpenCC

from ocr import *
from export import *
from function import *


app = Flask(__name__)

# file storage
UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# 500MB limit for single upload
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024


# verify file extensions
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html', template_folder='./')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    cc = OpenCC('s2tw')

    if request.method == 'POST':
        uploaded_files = request.files.getlist("file[]")
        filenames = []
        ocr_results = []
        ocr_list_result = []
        ocr_final_result = str()
        counter = 1

    for file in uploaded_files:
        if file and allowed_file(file.filename):
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
        counter += 1

    for f in ocr_list_result:
        ocr_final_result = ocr_final_result + str(f)

    txt_export_web(ocr_final_result)

    return render_template('result.html',
                           filenames=filenames,
                           ocr_final_result=ocr_final_result)


@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/download')
def download_txt():
    return send_file(
        'download/output.txt',
        mimetype='text/plain',
        download_name='result.txt',
        as_attachment=True)


if __name__ == "__main__":
    file_cleanup("upload")

    app.run(debug=True, port=8000)
