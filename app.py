from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db' # Устанавливаем значение той базы данных с которой будем работать
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()


class Article(db.Model): # Выбираем определённую табличку базы данных
        id = db.Column(db.Integer, primary_key=True) # Поля базы данных и их настройки 
        title = db.Column(db.String(100), nullable=False) 
        intro = db.Column(db.String(300), nullable=False) #  Макс 300 символов и не может быть поле пустым
        text = db.Column(db.Text, nullable=False) 
        date = db.Column(db.DateTime, default=datetime.utcnow) 

        def __repr__(self):
            return '<Article %r>' % self.id # Выдаем сам объект и его id


@app.route('/') # Отслеживаем страничку
@app.route('/home') # =
def index():
    return render_template("index.html") # Выводим html страницу


@app.route('/about') # Отслеживаем страничку
def about():
    return render_template("about.html")


@app.route('/posts') # Отслеживаем страничку
def posts():
    articles = Article.query.order_by(Article.date.desc()).all() # Берем все данные из базы данных и сортируем по date
    return render_template("posts.html", articles=articles) # Передаем в шаблон articles

@app.route('/posts/<int:id>') # Отслеживаем страничку
def post_detail(id):
    article = Article.query.get(id) # Ищем обект
    return render_template("post_detail.html", article=article)

@app.route('/posts/<int:id>/del') # Отслеживаем страничку
def post_delete(id):
    article = Article.query.get_or_404(id) # Ищем объект если нету то вернем ошибку 404

    try:
        db.session.delete(article) # Удаляем из бд объект article
        db.session.commit() # Объект сохраняем
        return  redirect('/posts')
    except:
        return "При удалении статьи произошла ошибка"


@app.route('/posts/<int:id>/update', methods=['POST', 'GET']) # Отслеживаем страничку
def post_update(id):
    article = Article.query.get(id) # Ищем объект если нету то вернем ошибку 404
    if request.method == "POST": # Если отправил post запрос
         article.title  = request.form['title']
         article.intro  = request.form['intro']
         article.text  = request.form['text']
         try:
              db.session.commit() # обект сохроняем
              return  redirect('/posts')
         except Exception as e:
               return f"При редактировании статьи произошла ошибка: {e}"
    else:
        return render_template("post_update.html", article=article)



@app.route('/create-article', methods=['POST', 'GET']) # Отслеживаем страничку
def create_article():
    if request.method == "POST": # Если отправил post запрос
         title  = request.form['title']
         intro  = request.form['intro']
         text  = request.form['text']

         article = Article(title=title, intro=intro, text=text)

         try:
              db.session.add(article) # Добавляем объект
              db.session.commit() # Объект сохроняем
              return  redirect('/posts')
         except Exception as e:
               return f"При добавлении статьи произошла ошибка: {e}"
    else:
        return render_template("create-article.html")

# @app.route('/user/<string:name>/<int:id>') # Отслеживаем страничку и читаем url получая name и id
# def user(name, id):
#     return "User page " + name + ' - ' + str(id) # Выводим name и id


if __name__ == "__main__":
    app.run(debug=True)