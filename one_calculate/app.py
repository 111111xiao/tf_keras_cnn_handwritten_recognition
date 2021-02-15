# requests are objects that flask handles (get set post, etc)
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
# scientific computing library for saving, reading, and resizing images
import cv2 
# for matrix math
import numpy as np
# for regular expressions, saves time dealing with string data
import re
# system level operations (like loading files)
import sys
# for reading operating system data
import os
# for save file as sys time
import time
from datetime import timedelta
# for rank numbers
import fnmatch

# tell our app where our saved models are
import concom
import calcul

# initalize our flask app
app = Flask(__name__)

import base64
# decoding an image from base64 into raw representation
def convertImage(imgData1):
    imgstr = re.search(r'base64,(.*)', str(imgData1)).group(1)
    with open('output.png', 'wb') as output:
        output.write(base64.b64decode(imgstr))

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 
app.send_file_max_age_default = timedelta(seconds=1) 

def predict_fun(image, flag = 0):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # BINARY
    ret,image = cv2.threshold(image,127,255,cv2.THRESH_BINARY)
    response = []
    responses = concom.make_predict(image, response)
    print(str(response))
    new_list = calcul.judge(response)  
    if flag == 1:
        responses.insert(0,'$')
        new_list.append('$')
    responses.extend(new_list)
    res = ''.join(responses)
    print(str(res))
    return res

@app.route('/', methods=['POST', 'GET'])
def index():
    error = 'status'
    if request.method == 'POST':
        f = request.files['file']
 
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "only png"})
 
        basepath = os.path.dirname(__file__)  
 
        upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))
        f.save(upload_path)
 
        img = cv2.imread(upload_path)
        cv2.imwrite(os.path.join(basepath, 'static/images', 'output.png'), img)
        new_image = cv2.imread('./static/images/output.png')
        res = predict_fun(new_image)
 
        return render_template("upload_ok.html", res = res, val1=time.time())
        
    return render_template("index.html", error = error)

@app.route('/picture/', methods = ["POST","GET"])
def picture():
    error = "no data"
    if request.method == 'POST':
        f = request.files['file']
        if not (f and allowed_file(f.filename)):
                return jsonify({"error": 1001, "msg": "only png"})
      
        basepath = os.path.dirname(__file__)  
      
        upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))
        f.save(upload_path)
      
        img = cv2.imread(upload_path)
        cv2.imwrite(os.path.join(basepath, 'static/images', 'output.png'), img)
        new_image = cv2.imread('./static/images/output.png')
        res = predict_fun(new_image, flag = 1)
        return res
    return error
  
@app.route('/predict/', methods=['GET', 'POST'])
def predict():

    imgData = request.get_data()

    convertImage(imgData)

    new_image = cv2.imread('output.png')

    res = predict_fun(new_image, flag = 1)
    return res

# draw multi dataset
DIR = './x'

def convertImage2(imgData2, name):
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    path = os.path.join(DIR)
    imgstr2 = re.search(r'base64,(.*)', str(imgData2)).group(1)
    print(os.path.join(path,name + now + '.png'))
    with open(os.path.join(path,name + now + '.png'), 'wb') as output:
        output.write(base64.b64decode(imgstr2))
        return True

@app.route('/login/', methods = ['POST', 'GET'])
def login():
    error = None
    users = ['xiaoli','boshi','dage','haoliu']
    if request.method == 'POST':
        for user in users:
            if (user == request.form['username']):
                return redirect(url_for('success', name = request.form['username']))
            else :
                error = 'Invalid username or password. Please try again!'
    return render_template('login.html', error = error)

@app.route('/success/<name>')
def success(name = None):
    users = ['xiaoli','boshi','dage','haoliu']
    for user in users:
        if (user == name):
            lis = os.listdir(DIR)
            rank_list = [len(fnmatch.filter(lis, x+'*')) for x in users]
            print(rank_list)
            return render_template('index2.html', name = name, rank_list = rank_list)
        else:
            error = 'Unknown username'
    return render_template('login.html', error = error)
    
@app.route('/pred/<name>', methods=['GET', 'POST'])
def predict2(name):
    respon = 'false'
    imgData2 = request.get_data()
    lis = os.listdir(DIR)
    if len(lis) <= 4096:
        if convertImage2(imgData2, name):
            respon = 'save success'
            return respon + str(len(lis))
    else:
        respon = 'image is full please ask xiaoli'
    return respon


if __name__ == "__main__":
    # run the app locally on the given port
    app.run(host='0.0.0.0', port=5000, debug=True)
# optional if we want to run in debugging mode
# app.run(debug=True)