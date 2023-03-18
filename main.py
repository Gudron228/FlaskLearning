from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session
from databases import mainmenu, posts


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdfjn2jh4b34h2k3jb2k4j2b'

metadata = MetaData()

engine = create_engine("mysql+pymysql://root:vovik2003@localhost/test")
session = Session(bind=engine)


def get_db():
    if not hasattr(g, 'db'):
        g.db = engine.connect()
    return g.db


def get_Menu():
    try:
        res = session.query(mainmenu).all()
        print(res)
        if res: return res
    except:
        print("Ошибка чтения из БД")
    return []


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()


@app.route("/")
def index():
    db = get_db()
    dbase = get_Menu()
    return render_template('index.html', menu=dbase)


@app.route("/add_post", methods=["POST", "GET"])
def add_post():
    db = get_db()
    dbase = get_Menu()
    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            flash('Сообщение отправлено', category='success')
        else:
            flash('Ошибка отправки', category='error')
        print(request.form)

    return render_template('add_post.html', title="Добавить статью", menu=dbase)


@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return render_template('cab.html', title="Личный кабинет", usrnm=username)


@app.route("/login", methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'admin' and request.form['psw'] == '1234567':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('login.html', title="Авторизация")


@app.errorhandler(404)
def page_notfound(error):
    return render_template('page404.html', title="Страница не найдена")


if __name__ == "__main__":
    app.run(debug=True)
