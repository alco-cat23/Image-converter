from flask import Flask, render_template, request, send_file
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'

# Создаем папки для загрузок и результатов, если их нет
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'Нет файла для загрузки', 400

    file = request.files['file']

    if file.filename == '':
        return 'Нет выбранного файла', 400

    if file and file.filename.endswith('.png'):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Конвертируем PNG в JPG
        img = Image.open(file_path)
        jpg_filename = f"{os.path.splitext(file.filename)[0]}.jpg"
        jpg_path = os.path.join(RESULT_FOLDER, jpg_filename)

        img.convert('RGB').save(jpg_path, 'JPEG')

        return send_file(jpg_path)

    return 'Неподдерживаемый формат файла. Пожалуйста, загрузите PNG.', 400


if __name__ == '__main__':
    app.run(debug=True)