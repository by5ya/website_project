from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///LostCatsBlog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy()
db.init_app(app)

# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Cat(db.Model):  # Replace Cat with your actual model
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(80), nullable=False)
        age = db.Column(db.Integer)
        description = db.Column(db.String(80), nullable=False)
        image_url = db.Column(db.String(80), nullable=False)

        def __repr__(self):
            return f"<Cat {self.name}>"

    # Create the database tables *only once* when the app starts.  Important!
with app.app_context():
    db.create_all()
    # Add some data (only needed once)
    if not Cat.query.first():  # Check if any cats exist first
        new_cat = Cat(name="Whiskers", age=2, description="Милый котик", image_url="static/img/img1.jpeg")
        new_cat1 = Cat(name="Bobby", age=2, description="Милый котик еще один", image_url="static/img/img2.jpeg")
        db.session.add(new_cat)
        db.session.commit()
        db.session.add(new_cat1)
        db.session.commit()


@app.route('/catalog')
def get_cat():
    print("Retrieving cats")
    cats = Cat.query.all()
    print(f"Cats: {cats}")  # Inspect the cats in the console.
    return render_template('get_cat.html', cats=cats)



@app.route('/')
def home_page():
    return render_template('home_page.html')


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

if __name__ == '__main__':
    app.run(debug=True)