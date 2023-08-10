import os
import shutil

from flask import Flask
from flask import render_template
from flask import request
from werkzeug.utils import secure_filename
from flask import send_from_directory
from opencc import OpenCC

from ocr import *
from export import *


app = Flask(__name__)

# file storage
UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# 500MB limit for single upload
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024


# clean up the directory on the website startup
def file_cleanup(directory):
    folder = directory

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)

        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


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
        image_number = len(uploaded_files)
        image_number_modular = image_number % 7

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

    return render_template('result.html',
                           filenames=filenames,
                           ocr_final_result=ocr_final_result,
                           image_number=image_number,
                           image_number_modular=image_number_modular)


@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    file_cleanup("upload")
    file_cleanup("download")
    file_cleanup("opencv")

    app.run(debug=True, port=8000)
