# -*- coding: utf-8 -*-
#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, send_file
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user
from werkzeug.security import check_password_hash
from logger import logger
from get_def import split_phones

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB 
app.secret_key = b'HelloWorld'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Пользователь для проверки авторизации
class User(UserMixin):
    def __init__(self, password_hash):
        self.id = 1
        self.password_hash = password_hash

user = User('pbkdf2:sha256:260000$vtfTXdL1op0lCRqk$f1526865a50f696bbee79a5485ff19308d9a3a3a0faa20c97127924a7d13a3a9')

@login_manager.user_loader
def load_user(id):
    return user

@app.route('/login', methods=['get', 'post'])
def login():
    if (current_user.is_authenticated):
        return redirect('/')

    if request.method == 'GET':
        return render_template('index.html')

    candidate_password = request.form.get('password', '').strip()
    logger.debug(f'Получен запрос на авторизацию. Пароль: {candidate_password}')

    if (check_password_hash(user.password_hash,  candidate_password)):
        login_user(user, remember=True)
        logger.debug(f'Успешно, запоминаем и возвращаем на главную')
        return redirect('/')

    return render_template('index.html'), 401

@app.route('/', methods=['get', 'post'])
@login_required
def upload():
    if request.method == 'GET':
        return render_template('index.html')
  
    file = request.files.get('phoneList', None)
    logger.info(f'Получен новый файл: {file.content_length}')

    if file is None:
      return redirect(request.url)

    logger.debug(f'Начинаем читать и делить файл')
    try:
        buffer = split_phones(file)
    except:
        logger.exception('Ошибка при обработке файла');
        return 'Internal error', 500

    return send_file(
        buffer,
        attachment_filename='name',
        as_attachment=True,
        mimetype='text/csv'
        )

if __name__ == '__main__':
    app.run(debug=True)
