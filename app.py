from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

database = SQLAlchemy(app)

class Users(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String(100), unique=True)
    psw = database.Column(database.String(100), nullable=True)
    date = database.Column(database.DateTime, default=datetime.utcnow)

    hook = database.relationship('Profiles', backref='users', uselist=False)

    def __repr__(self):
        return f'<User {self.id}>'
    
class Profiles(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(100), nullable=True)
    old = database.Column(database.Integer)
    city = database.Column(database.String(100))

    user_id = database.Column(database.Integer, database.ForeignKey('users.id'))

    def __repr__(self):
        return f'<Profile {self.id}>'
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            user = Users(email=request.form['email'], psw=request.form['psw'])
            database.session.add(user)
            database.session.flush()

            profile = Profiles(name=request.form['name'], old=request.form['old'], city=request.form['city'], user_id=user.id)
            database.session.add(profile)
            database.session.commit()
            
        except:
            database.session.rollback()
            print('Ошибка записи в базу данных')

    return render_template('register.html')

with app.app_context():
    database.create_all()

if __name__ == '__main__':
    
    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/register', 'register', register)
    app.run(debug=True)