from flask import Flask, render_template

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cats.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


class Cat(db.Model):  # Replace Cat with your actual model
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(80), nullable=False)

        def __repr__(self):
            return f"<Cat {self.name}>"


    # Create the database tables *only once* when the app starts.  Important!
with app.app_context():
    db.create_all()
    # Add some data (only needed once)
    if not Cat.query.first():  # Check if any cats exist first
        new_cat = Cat(name="Whiskers")
        db.session.add(new_cat)
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

@app.route('/registry')
def registry():
    return render_template('registry.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)