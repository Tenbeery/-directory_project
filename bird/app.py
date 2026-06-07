from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# НАСТРОЙКИ ДЛЯ ЗАГРУЗКИ ФАЙЛОВ
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Создаём папку для загрузок, если её нет
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Путь к файлу данных
DATA_FILE = os.path.join('data', 'birds.json')


def allowed_file(filename):
    """Проверяет, разрешён ли тип файла"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_birds():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_birds(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/handbook')
def handbook():
    data = load_birds()
    return render_template('info.html', data=data)


@app.route('/add', methods=['GET', 'POST'])
def add_bird():
    if request.method == 'POST':
        # Получаем данные из текстовых полей
        name = request.form.get('name')
        latin = request.form.get('latin')
        habitat = request.form.get('habitat')
        desc = request.form.get('desc')

        # Обработка загруженного файла
        image_filename = "default.jpg"  # значение по умолчанию

        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                image_filename = file.filename
                # Сохраняем файл в папку static/uploads
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        # Создаём новую запись
        new_bird = {
            "name": name,
            "latin": latin,
            "habitat": habitat,
            "desc": desc,
            "image": image_filename
        }

        # Загружаем текущую базу, добавляем птицу и сохраняем
        data = load_birds()
        data['birds'].append(new_bird)
        save_birds(data)

        # После добавления перенаправляем пользователя в справочник
        return redirect(url_for('handbook'))

    return render_template('add.html')


if __name__ == '__main__':
    app.run(debug=True)