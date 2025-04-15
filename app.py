from datetime import datetime
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, current_app
from models import db, Cat, User, News

from werkzeug.utils import secure_filename


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///LostCatsBlog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/img'


db.init_app(app)


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
        name = request.form['name']
        age = request.form['age']
        description = request.form['description']
        image = request.files['image_file']
        if image:
                filename = secure_filename(image.filename)  # Sanitize filename
                filepath = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'] + "/cats", filename)
                image.save(filepath)
                img_url = url_for('static', filename='img/cats/' + filename)
                cat = Cat(name=name, age=age, description=description, image_url=img_url)
                db.session.add(cat)
                db.session.commit()
                return redirect(url_for('add_cat'))
    return render_template('add_cat.html')

@app.route('/delete_cat/<int:cat_id>', methods=['POST'])  # Use POST for deletion
def delete_cat(cat_id):

    cat = Cat.query.get_or_404(cat_id)  # Get cat or return 404 if not found

    db.session.delete(cat)
    db.session.commit()

    return redirect(url_for('admin_page'))

@app.route('/delete_cat_page')  # Use POST for deletion
def delete_cat_page():
    cats = Cat.query.all()
    return render_template('delete_cat_page.html', cats=cats)


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