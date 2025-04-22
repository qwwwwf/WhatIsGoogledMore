from os import getenv
from dotenv import load_dotenv

from api.user_api import UserResource
from config import STAR_EXCHANGE_RATE
from data import db_session
from data.user_model import User

from flask_restful import Api
from flask import Flask, render_template, redirect
from flask_login import LoginManager, logout_user, login_required, login_user, current_user

from forms.login_form import LoginForm
from forms.register_form import RegisterForm

load_dotenv()

# Flask app init
app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY', '0b2d776d7d3e50323e285c30f9c3afce')

# API
api = Api(app)
api.add_resource(UserResource, '/api/users/<user_id>/<action>')

# Database init
db_session.global_init('db/data.db')

# Login manager init
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


# Routes
@app.route('/', methods=['GET', 'POST'])
def index_route():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login_route():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template(
            'login.html',
            message="Неправильный логин или пароль",
            form=form)
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register_route():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template(
                'register.html',
                title='Регистрация',
                form=form,
                message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.username == form.username.data).first():
            return render_template(
                'register.html',
                title='Регистрация',
                form=form,
                message="Такой пользователь уже есть")

        user = User(username=form.username.data)

        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')

    return render_template('register.html', form=form)


@app.route('/profile', methods=['GET', 'POST'])
def profile_route():
    games_data = []

    for game in current_user.games:
        games_data.append([game.id, game.total_rounds, game.correctly_rounds, game.points_gave])

    return render_template(
        'profile.html',
        games=games_data,
        games_count=len(games_data)
    )


@app.route('/top', methods=['GET', 'POST'])
def top_route():
    db_sess = db_session.create_session()
    users = db_sess.query(User).order_by(User.stars.desc()).limit(15)
    top_data = []

    for user in users:
        top_data.append([user.username, user.stars, len(user.games)])

    for i in range(len(top_data)):
        top_data[i].insert(0, i + 1)

    return render_template(
        'top.html',
        users=top_data
    )


@app.route('/exchange', methods=['GET', 'POST'])
def exchange_route():
    return render_template(
        'exchange.html',
        exchange_history=current_user.exchange_history['exchanges'],
        exchange_rate=STAR_EXCHANGE_RATE
    )

@app.route('/play', methods=['GET', 'POST'])
def play_route():
    return render_template('game.html')


# App run
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
