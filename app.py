from datetime import datetime
import os
import sys
from flask import Flask, render_template, request, redirect, url_for, flash, session, current_app
from models import db, Cat, User, News
import requests
from werkzeug.utils import secure_filename


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///LostCatsBlog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/img'
app.config["SECRET_KEY"]="SECRET"
static_map_server = 'https://static-maps.yandex.ru/v1?'
geocoder_server = 'http://geocode-maps.yandex.ru/1.x/?'
apikey_geocode = "8013b162-6b42-4997-9691-77b7074026e0"
apikey_static = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/catalog')
def get_cat():
    print("Retrieving cats")
    cats = Cat.query.all()
    print(f"Cats: {cats}")  # Inspect the cats in the console.
    return render_template('get_cat.html', cats=cats)



@app.route('/')
def home_page():
    news = News.query.all()
    return render_template('home_page.html', news=news)


@app.route('/info')
def about():
    return render_template('about.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/registry', methods=['GET', 'POST'])
def registry():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Пароли не совпадают')
            return redirect(url_for('registry'))
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Имя пользователя уже занято')
            return redirect(url_for('registry'))
        
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email уже зарегистрирован')
            return redirect(url_for('registry'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Регистрация успешна! Теперь можно войти.')
        return redirect(url_for('login'))
    
    return render_template('registry.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Добро пожаловать!')
            return redirect(url_for('home_page'))
        else:
            flash('Неверные данные')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Вы вышли из аккаунта')
    return redirect(url_for('home_page'))

@app.route('/add_cat', methods=['GET', 'POST'])
def add_cat():
    if request.method == 'POST':
        cat_name = request.form['name']
        age = request.form['age']
        description = request.form['description']
        address = request.form['address']
        image = request.files['image_file']
        if image:
            filename = secure_filename(image.filename)  
            filepath = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'] + "/cats", filename)
            image.save(filepath)

            img_url = url_for('static', filename='img/cats/' + filename)

            response = requests.get(f'{geocoder_server}apikey={apikey_geocode}&geocode={address}&format=json')
            if not response:
                    print("Ошибка выполнения запроса:")
                    print(response)
                    print("Http статус:", response.status_code, "(", response.reason, ")")
                    sys.exit(1)
            if response:
                json_response = response.json()
                toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                toponym_coordinates = toponym["Point"]["pos"]  # Исправлено опечатку
                print(toponym_coordinates)  # Отладочный вывод
                try:
                    longitude, latitude = map(float, toponym_coordinates.split())  # Преобразуем в числа
                except ValueError:
                    print("Ошибка: Не удалось преобразовать координаты в числа.")
                    address_img_url = None
                    # Дальнейшая обработка ошибки (например, запись в лог)
                    return  # Или другое действие для выхода из функции

                print(f"Широта: {latitude}, Долгота: {longitude}") #Отладочный вывод

                # Формируем строку запроса с правильным порядком координат и числовыми значениями
                ll_spn = f'll={longitude},{latitude}&spn=0.002,0.002&size=300,300'  # Порядок: широта, долгота
                response1 = requests.get(f'{static_map_server}{ll_spn}&apikey={apikey_static}', stream=True) 
                if not response1.ok: # Лучше проверять response1.ok
                    print("Ошибка выполнения запроса к static-maps:")
                    print(response1.text) # Выводим текст ошибки
                    print("Http статус:", response1.status_code, "(", response1.reason, ")")
                    sys.exit(1)

                map_file = f'{cat_name}_address.png'
                address_folder = os.path.join(current_app.root_path, 'static', 'img', 'address') # Более надежный путь
                os.makedirs(address_folder, exist_ok=True) # Создаем папку, если ее нет

                filepath = os.path.join(address_folder, map_file) # Полный путь к файлу
                print(f"Сохраняем карту в: {filepath}") # Отладочный вывод

                try:
                    with open(filepath, "wb") as file:
                        for chunk in response1.iter_content(chunk_size=8192):  # Сохраняем по частям (важно для больших файлов)
                            file.write(chunk)
                except Exception as e:
                    print(f"Ошибка при записи файла: {e}")
                    sys.exit(1)


                address_img_url = url_for('static', filename=f'img/address/{map_file}')  # Правильный путь для url_for
                print(f"URL к картинке: {address_img_url}") #Отладочный вывод
            else:
                address_img_url = None # Или какое-то значение по умолчанию, если не удалось получить адрес
            cat = Cat(name=cat_name, age=age, description=description, image_url=img_url, address_img_url=address_img_url, address=address)
            db.session.add(cat)
            db.session.commit()
            return redirect(url_for('add_cat'))
    return render_template('add_cat.html')

@app.route('/delete_cat/<int:cat_id>', methods=['POST'])  # Use POST for deletion
def delete_cat(cat_id):

    cat = Cat.query.get_or_404(cat_id)  # Get cat or return 404 if not found
    try:
        # Удаляем файл картинки кота, если он существует
        if cat.image_url:  # Проверяем, есть ли путь к изображению
            image_url = os.path.join(current_app.root_path, 'static', cat.image_url)
            if os.path.exists(image_url):
                os.remove(image_url)

        # Удаляем файл картинки адреса, если он существует
        if cat.address_img_url:  # Проверяем, есть ли путь к изображению адреса
            address_img_url = os.path.join(current_app.root_path, cat.address_img_url )
            print(address_img_url)
            if os.path.exists(address_img_url):
                os.remove(address_img_url)

        # Удаляем запись из базы данных
        db.session.delete(cat)
        db.session.commit()

    except Exception as e:
        db.session.rollback()  # Откатываем изменения в БД при ошибке
        current_app.logger.error(f"Error deleting cat {cat_id}: {str(e)}")
        # Можно добавить flash-сообщение об ошибке
        flash('Произошла ошибка при удалении кота', 'error')

    return redirect(url_for('admin_page'))

@app.route('/delete_cat_page')  # Use POST for deletion
def delete_cat_page():
    cats = Cat.query.all()
    return render_template('delete_cat_page.html', cats=cats)


@app.route('/get_cat_home/<int:cat_id>')
def get_cat_home(cat_id):
    cat = Cat.query.get_or_404(cat_id)
    print(cat.address_img_url)
    return render_template('get_cat_home.html', cat=cat)


@app.route('/delete_news/<int:new_id>', methods=['POST'])  # Use POST for deletion
def delete_new(new_id):

    new = News.query.get_or_404(new_id)  # Get cat or return 404 if not found

    db.session.delete(new)
    db.session.commit()

    return redirect(url_for('admin_page'))

@app.route('/delete_news_page')  # Use POST for deletion
def delete_news_page():
    news = News.query.all()
    return render_template('delete_news_page.html', news=news)
    
@app.route('/admin_page') 
def admin_page():
    return render_template('admin_page.html')


@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    if request.method == 'POST':
        title = request.form['title']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        content = request.form['content']
        image = request.files['image_file']
        if image:
                filename = secure_filename(image.filename)  # Sanitize filename
                filepath = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'] + "/news", filename)
                image.save(filepath)
                img_url = url_for('static', filename='img/news/' + filename)
                news = News(title=title, date=date, content=content, image_url=img_url)
                db.session.add(news)
                db.session.commit()
                return redirect(url_for('add_news'))
    return render_template('add_news.html')

@app.route('/admin_pass', methods=['GET', 'POST'])
def admin_pass():
    if request.method == 'POST':
        password = request.form['password_admin']
        if password == 'admin':
            return render_template('admin_page.html')
    return render_template('admin_pass.html')



if __name__ == '__main__':
    app.run(debug=True)