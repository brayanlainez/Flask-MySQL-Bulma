import os
from flask import Flask, flash, session, request, make_response, render_template, abort, redirect, url_for, jsonify, json
from markupsafe import escape, Markup
from werkzeug.utils import secure_filename
from flaskext.mysql import MySQL
import pymysql

UPLOAD_FOLDER = './static/files/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__, template_folder='templates')

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'dbproductos'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql = MySQL()
mysql.init_app(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# app.logger.debug('A value for debugging')
# app.logger.warning('A warning occurred (%d apples)', 42)
# app.logger.error('An error occurred')

@app.route('/')
def index():
    # username = request.cookies.get('username')
    current_user = None
    if 'username' in session:
        current_user = escape(session['username'])
    resp = make_response(render_template('index.html', current_user = current_user))
    # resp.set_cookie('username', 'username')
    return resp

@app.route('/login', methods=['GET','POST'])
def login():
    # abort(401)
    if request.method == 'POST':
        if request.form['username'] == 'admin@mail.com' and request.form['password'] == 'password':
            session['username'] = request.form['username']
            flash('You were successfully logged in','success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password','danger')
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/about/')
@app.route('/about/<name>')
def about(name=None):
    return render_template('about.html', name=name)

@app.route('/products/', methods=['GET','POST','PUT'])
@app.route('/products/<int:id>', methods=['GET','DELETE'])
def products(id=None):
    if request.method == 'GET':
        try:
            product=None
            cursor = mysql.get_db().cursor()
            cursor.execute("SELECT id, nombre, codigo_barra, precio, disponible, detalle, imagen FROM tbl_productos;")
            products=cursor.fetchall()
            if id:
                cursor.execute("SELECT id, nombre, codigo_barra, precio, disponible, detalle, imagen FROM tbl_productos WHERE id= {0};".format(escape(id)))
                product=cursor.fetchall()
                product=product[0]
            return render_template('products.html', products=products, product=product)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
    elif request.method == 'POST':
        try:
            nombre = request.form['nombre']
            codigo_barra = request.form['codigo_barra']
            precio = request.form['precio']
            disponible = request.form['disponible']
            detalle = request.form['detalle']

            file = request.files['imagen']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                imagen = 'files/'+filename
                url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(url)

            cursor = mysql.get_db().cursor()
            cursor.execute("INSERT INTO tbl_productos(nombre, codigo_barra, precio, disponible, detalle, imagen) VALUES (%s, %s, %s, %s, %s, %s);",
            (nombre, codigo_barra, precio, disponible, detalle, imagen))
            mysql.get_db().commit()
            flash('¡Added successfully!','success')
            return redirect(url_for('products'))
        except Exception as e:
            print(e)
        finally:
            cursor.close()
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass

@app.route('/product_put/', methods=['POST'])
def product_put():
    if request.method == 'POST':
        try:
            id = request.form['id']
            nombre = request.form['nombre']
            codigo_barra = request.form['codigo_barra']
            precio = request.form['precio']
            disponible = request.form['disponible']
            detalle = request.form['detalle']

            file = request.files['imagen']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                imagen = 'files/'+filename
                url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(url)

            cursor = mysql.get_db().cursor()
            cursor.execute("UPDATE tbl_productos SET nombre=%s, codigo_barra=%s, precio=%s, disponible=%s, detalle=%s, imagen=%s WHERE id= %s",
            (nombre, codigo_barra, precio, disponible, detalle, imagen, id))
            mysql.get_db().commit()
            flash('¡Updated successfully!','success')
            return redirect(url_for('products'))
        except Exception as e:
            print(e)
        finally:
            cursor.close()

@app.route('/product_delete/<int:id>')
def product_delete(id):
    try:
        cursor = mysql.get_db().cursor()
        cursor.execute("DELETE FROM tbl_productos WHERE id = {0};".format(escape(id)))
        mysql.get_db().commit()
        flash('¡Deleted successfully!','danger')
        return redirect(url_for('products'))
    except Exception as e:
        print(e)
    finally:
        cursor.close()

@app.errorhandler(404)
def page_not_found(error):
    resp = make_response(render_template('page_not_found.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return 'Subpath {}'.format(escape(subpath))

@app.route('/uuid/<uuid:id>')
def uuid(id):
    return 'UUID = %s' % escape(id)

# with app.test_request_context():
#     print(url_for('products', id=1))
#     print(url_for('index'))
#     print(url_for('login'))
#     print(url_for('login', next='/'))
#     print(url_for('static', filename='style.css'))

with app.test_request_context('/hello', method='POST'):
    # now you can do something with the request until the
    # end of the with block, such as basic assertions:
    assert request.path == '/hello'
    assert request.method == 'POST'

# with app.request_context(environ):
#     assert request.method == 'POST'

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host='127.0.0.1', port=port, debug=True, load_dotenv=True)