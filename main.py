from os import getenv
from dotenv import load_dotenv

from data import db_session
from data.user_model import User

from flask import Flask, render_template, redirect
from flask_login import LoginManager, logout_user, login_required, login_user

from forms.login_form import LoginForm
from forms.register_form import RegisterForm

load_dotenv()

# Flask app init
app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY')

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
@app.route('/')
def index_route():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template(
            'login.html',
            message="Неправильный логин или пароль",
            form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template(
                'register.html',
                title='Регистрация',
                form=form,
                message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter((User.email == form.email.data) | (User.username == form.username.data)).first():
            return render_template(
                'register.html',
                title='Регистрация',
                form=form,
                message="Такой пользователь уже есть")

        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )

        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')

    return render_template('register.html', title='Регистрация', form=form)


# App run
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
