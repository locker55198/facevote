import os

from flask import (Flask, redirect, render_template, request, jsonify, send_from_directory, url_for)
from conn import save_to_database

app = Flask(__name__)

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('name')
        image = request.files['image'].read()  # 獲取上傳的圖片文件並讀取其內容
        save_to_database(name, image)  # 假設有一個名為save_to_database的函數來處理數據保存
        return jsonify({'message': 'Registration successful'})

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/vote')
def vote():
    return render_template('vote.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
