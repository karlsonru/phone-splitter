from flask import Flask, render_template, request, flash, redirect, send_file
import get_def

app = Flask(__name__)

# 16 MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

@app.get('/')
def hello():
    return render_template('index.html')

@app.post('/')
def get_file():
  file = request.files.get('phoneListFile', None)

  if file is None:
    flash('No file selected for uploading')
    return redirect(request.url)

  buffer = get_def.split_phones(file)

  return send_file(
    buffer,
    download_name='flask_hello.csv',
    as_attachment=True,
    mimetype='text/csv'
    )