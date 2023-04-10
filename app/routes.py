from flask import render_template, request, flash, abort, redirect, url_for, g
from app import app
from app.forms import LoginForm, AddPostForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import MainMenu, Users, Posts
from app import db
from app.methods import getUserByEmail, get_menu, get_post, getPostsAnounce
from flask_login import current_user, login_user, login_required, logout_user

dbase = None

@app.before_request
def before_request():
    global dbase
    dbase = get_menu()

@app.route("/")
@app.route("/index")
@login_required
def index():
    return render_template('index.html', menu=dbase, posts=getPostsAnounce())


@app.route("/add_post", methods=["POST", "GET"])
def add_post():
    form = AddPostForm()
    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            post = Posts(
                title=request.form['name'],
                text=request.form['post'])
            db.session.add(post)
            db.session.commit()
            if not post:
                flash('Ошибка добавления статьи', category='error')
            else:
                flash('Статья успешно добавлена', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')

    return render_template('add_post.html', title="Добавить новость", menu=dbase, form=form)


@app.route("/post/<int:id_post>")
def showPost(id_post):
    id, title, post, time = get_post(id_post)
    if not title:
        abort(404)
    return render_template('post.html', menu=dbase, title=title, post=post)


@app.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = Users(
            name=request.form['name'],
            email=request.form['email'],
        )
        user.set_password(request.form['password'])
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрированы', category='success')
        return redirect(url_for('login'))
        if not user:
            flash('Ошибка добавления в БД', category='error')
    else:
        flash('Ошибка регистрации', category='error')

    return render_template('register.html', menu=dbase, title="Регистрация", form=form)


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = getUserByEmail(request.form['email'])
        if user and user.check_password(request.form['password']):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
        else:
            flash('Неправильный email или пароль')
            return redirect(url_for('login'))

    return render_template('login.html', menu=dbase, title="Авторизация", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_notfound(error):
    return render_template('page404.html', title="Страница не найдена", menu=dbase)
