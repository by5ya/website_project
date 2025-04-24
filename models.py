
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Cat(db.Model):  # Replace Cat with your actual model
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(80), nullable=False)
        age = db.Column(db.Integer)
        description = db.Column(db.String(80), nullable=False)
        image_url = db.Column(db.String(80), nullable=False)
        address = db.Column(db.String(80), nullable=False)
        address_img_url = db.Column(db.String(80), nullable=False)

        def __repr__(self):
            return f"<Cat {self.name}>"
        

class News(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(300), nullable=False)
        date = db.Column(db.DateTime, nullable=False, default=datetime.now)  # Date and time, default to now
        content = db.Column(db.Text, nullable=False)  # Full text of the news
        image_url = db.Column(db.String(500), nullable=True) #URL to image

        def __repr__(self):
             return f'News {self.title}'

        


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