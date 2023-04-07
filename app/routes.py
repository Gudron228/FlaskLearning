from flask import render_template, request, flash, abort, redirect, url_for, g
from app import app
from app.forms import LoginForm, AddPostForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required
from sqlalchemy import select, desc
from app.models import MainMenu, Users, Posts
from flask import session
from sqlalchemy.orm import session, Session
from app import db



def get_menu():
    try:
        res = MainMenu.query.all()
        print(res)
        if res:
            return res
    except:
        print("Ошибка чтения из БД")
    return []


def getPostsAnounce():
    try:
        res = Posts.query.order_by(desc(Posts.datetime)).all()
        print(res)
        if res:
            return res
    except Exception as ex:
        print("Ошибка чтения из БД", ex)
    return []


def get_post(post_id):
    try:
        res = Posts.query(Posts.title, Posts.text).where(Posts.c.id == post_id).one()
        print(res)
        if res:
            return res
    except Exception as ex:
        print("Ошибка чтения из БД", ex)

    return False


def getUserByEmail(email):
    try:
        row = Users.query.where(Users.email == email).one()
        if not row:
            print("Пользователь не найден")
            return False
        return row
    except Exception as ex:
        print("Ошибка чтения из БД", ex)

    return False


def get_db():
    if not hasattr(g, 'db'):
        g.db = session.conect()
    return g.db


dbase = None


@app.before_request
def before_request():
    global dbase
    dbase = get_menu()


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()


@app.route("/")
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
@login_required
def showPost(id_post):
    title, post = get_post(id_post)
    if not title:
        abort(404)
    return render_template('post.html', menu=dbase, title=title, post=post)


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['email']) > 4 \
                and len(request.form['password']) > 4 and request.form['password'] == request.form['password2']:
            psw = generate_password_hash(request.form['password'])
            user = Users(
                name=request.form['name'],
                email=request.form['email'],
                password=psw

            )
            db.session.add(user)
            db.session.commit()
            if not user:
                flash('Ошибка добавления в БД', category='error')
            else:
                flash('Вы успешно зарегистрированы', category='success')
                return redirect(url_for('login'))
        else:
            flash('Ошибка регистрации', category='error')

    return render_template('register.html', menu=dbase, title="Регистрация", form=form)


@app.errorhandler(404)
def page_notfound(error):
    return render_template('page404.html', title="Страница не найдена", menu=dbase)
