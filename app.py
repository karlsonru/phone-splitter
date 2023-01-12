from flask import Flask, render_template, request, flash, redirect, send_file, url_for
from flask_login import LoginManager, login_required, login_user, current_user, login_remembered
from Models import user
import get_def

app = Flask(__name__)

# 16 MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 
app.secret_key = b'GRhL5mPW'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return user

@app.route('/login', methods=['get', 'post'])
def login():
  if (current_user.is_authenticated):
    return redirect('/')

  if request.method == 'GET':
    return render_template('login.html')

  password = request.form.get('password', None)

  if (user.check_password(password)):
    login_user(user, remember=True)
    print('Hello')
    return redirect('/')

  return render_template('login.html')

@app.route('/', methods=['get', 'post'])
@login_required
def upload():
  if request.method == 'GET':
    return render_template('upload.html')
  
  file = request.files.get('phoneListFile', None)

  if file is None:
    return redirect(request.url)

  buffer = get_def.split_phones(file)

  return send_file(
    buffer,
    download_name='flask_hello.csv',
    as_attachment=True,
    mimetype='text/csv'
    )
