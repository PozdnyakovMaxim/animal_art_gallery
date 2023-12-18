from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = '***_999f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user' 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image_url = db.Column(db.String(300), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_to_collection', methods=['POST'])
def add_to_collection():
    if 'collection' not in session:
        session['collection'] = []
    image_name = request.form['image_name']
    session['collection'].append(image_name)
    return 'Изображение добавлено в коллекцию.'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('collection'))
        return 'Invalid username or password'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/collection')
def collection():
    if 'user_id' not in session:
        return redirect(url_for('login'))   
    if 'collection' not in session:
        session['collection'] = []
    with app.app_context():
        user_images = Image.query.filter_by(user_id=session['user_id']).all()
    return render_template('collection.html', collection=session['collection'], images=user_images)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

