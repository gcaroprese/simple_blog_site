from flask import Flask, render_template
from flask_mysqldb import MySQL
import re

app = Flask(__name__)

# DB Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'tu_usuario_mysql'
app.config['MYSQL_PASSWORD'] = 'tu_contraseña_mysql'
app.config['MYSQL_DB'] = 'tu_base_de_datos_mysql'

mysql = MySQL(app)

def slugify(s):
    """
    Generate a slug from the given string.
    """
    s = re.sub(r'[^\w\s-]', '', s).strip().lower()
    s = re.sub(r'[-\s]+', '-', s)
    return s

@app.route('/')
def index():
    # Getting DB data rom posts
    cur = mysql.connection.cursor()
    cur.execute("SELECT title, author, publication_date, content, slug FROM posts")
    posts = cur.fetchall()
    cur.close()
    return render_template('index.html', posts=posts)

@app.route('/post/<slug>')
def post(slug):
    cur = mysql.connection.cursor()
    cur.execute("SELECT title, author, publication_date, content FROM posts WHERE slug = %s", (slug,))
    post = cur.fetchone()
    cur.close()
    return render_template('post.html', post=post)

if __name__ == '__main__':
    app.run(debug=True)
