from app import app, db
from models import Cat

with app.app_context():
    db.create_all()  # Создаем таблицы, если они еще не созданы

    # Пример данных
    cat1 = Cat(name='Мурзик', age=2, breed='Сиамская', description='Очень дружелюбный кот.', image_url='https://example.com/cat1.jpg')
    cat2 = Cat(name='Барсик', age=3, breed='Персидская', description='Любит спать и есть.', image_url='https://example.com/cat2.jpg')
    cat3 = Cat(name='Котя', age=1, breed='Британская', description='Активный и игривый.', image_url='https://example.com/cat3.jpg')

    db.session.add(cat1)
    db.session.add(cat2)
    db.session.add(cat3)
    db.session.commit()