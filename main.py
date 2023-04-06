from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g
from sqlalchemy import create_engine, MetaData, desc
from sqlalchemy.orm import Session
from databases import mainmenu, posts
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

metadata = MetaData()

engine = create_engine("mysql+pymysql://root:vovik2003@localhost/test")
session = Session(bind=engine)


def get_db():
    if not hasattr(g, 'db'):
        g.db = engine.connect()
    return g.db


def get_menu():
    try:
        res = session.query(mainmenu).all()
        print(res)
        if res: return res
    except:
        print("Ошибка чтения из БД")
    return []


def post_add(title, text):
    try:
        ins = posts.insert().values(
            title=title,
            text=text
        )
        session.execute(ins)
        session.commit()
    except Exception as ex:
        print('Ошибка:', ex)
        return False

    return True


def get_post(postId):
    try:
        res = session.query(posts.c.title, posts.c.text).filter(posts.c.id == postId).one()
        print(res)
        if res:
            return res
    except Exception as ex:
        print("Ошибка чтения из БД", ex)

    return (False, False)



def getPostsAnounce():
    try:
        res = session.query(posts).order_by(desc(posts.c.time)).all()
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
    dbase = get_menu()
    return render_template('index.html', menu=dbase, posts=getPostsAnounce())


@app.route("/add_post", methods=["POST", "GET"])
def add_post():
    db = get_db()
    dbase = get_menu()
    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = post_add(request.form['name'], request.form['post'])
            if not res:
                flash('Ошибка добавления статьи', category='error')
            else:
                flash('Статья успешно добавлена', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')

    return render_template('add_post.html', title="Добавить статью", menu=dbase)


@app.route("/post/<int:id_post>")
def showPost(id_post):
    db = get_db()
    dbase = get_menu()
    title, post = get_post(id_post)
    if not title:
        abort(404)
    return render_template('post.html', menu=dbase, title=title, post=post)


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
    db = get_db()
    dbase = get_menu()
    return render_template('page404.html', title="Страница не найдена", menu=dbase)


if __name__ == "__main__":
    app.run(debug=True)
