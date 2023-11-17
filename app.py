from flask import Flask, render_template, Response, request, jsonify
import cv2
import math
import time
import cvzone
import mysql.connector

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/video_feed')
def video_feed():
    return Response(detect_objects(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/vote')
def vote():
    return render_template('vote.html')

if __name__ == '__main__':
    app.run()
