from flask import request
from flask import Flask, render_template, jsonify, get_template_attribute, make_response,redirect
from flask import abort
from flask import session, url_for
# from werkzeug import secure_filename
# import numpy as np
import json
import time
from python.client import Client
import copy
import os

def getpath(digest):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'static/uploads', digest)

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home():
    if Client.username[0] == "":
        return redirect("/signin", code=302)
    if request.method == 'POST':
        postData = request.form.to_dict()
        print(postData)
        if "select_chatgroup" in postData:
            roomIDSelected = postData["select_chatgroup"]
            # Client.selectChatRoom(roomIDSelected)
            Client.currentRoomId[0] = roomIDSelected
            print('room select', roomIDSelected)
        if "send" in postData:
            if "message" in postData:
                contentMessage = postData["message"]
                Client.send_message(contentMessage)
                print('message', contentMessage)

            if "file" in request.files:
                print("file")
                fileMessage = request.files['file']
                Client.send_file(fileMessage)
            # filename = secure_filename(fileMessage.filename) 
    
    groupchat = render_template('groupchat.html', groups = Client.userRoomsData)
    sendbutton = render_template('sendbutton.html')
    if Client.currentRoomId[0] != "":
        log_ = Client.getRoomById(Client.currentRoomId[0])["log"]
        current_user = Client.username[0]
        contentchat = render_template('contentchat.html', logs = log_, usernames = current_user)
        groupName = f"<h1>{Client.getRoomById(Client.currentRoomId[0])['name']}</h1>"
        return render_template('index.html', groupchat = groupchat, sendbutton= sendbutton, contentchat =contentchat, groupName=groupName)
    else:
        contentchat = render_template('contentchat.html')
        return render_template('index.html', groupchat = groupchat, sendbutton= sendbutton, contentchat =contentchat)

@app.route('/signin', methods=['GET','POST'])
def signin():
    if Client.username[0] != "":
        return redirect("/", code=302)
    if request.method == 'POST':
        un = request.form['username']
        ps = request.form['password']
        res = Client.requestSignin(un, ps)
        if res:
            return redirect('/', code=302)
        else:
            signin = render_template('signin.html', failure=True)
            return render_template('index.html', signin = signin)
    else:
        signin = render_template('signin.html')
        return render_template('index.html', signin = signin)

@app.route('/signup', methods=['GET','POST'])
def signup():
    # print('sign_up')
    
    # signuphtml = render_template('signup.html')
    # print(render_template('index.html', signup = signup))
    # return render_template('signup.html')
    
    if request.method == 'POST':
        print('post')
        name=request.form['name']
        un = request.form['username']
        pw = request.form['password']
        gender=request.form['gender']
        print(name, un, pw, gender)
        res=Client.request_signup(name,un,pw,gender)
        print(res)
        if(res):
            Client.exist=True
            return redirect("/signin", code=302)
        else:
            return render_template('signup.html', state=True)
    else:         
        print('sign_up_2')
        return render_template('signup.html',state=False)

if __name__ == "__main__":
    # app.jinja_env.auto_reload = True
    # print(1000000)
    # app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="localhost", port=5001, debug=True, use_reloader=False)

# https://stackoverflow.com/questions/17057191/redirect-while-passing-arguments
# https://realpython.com/python-sockets/#background
# send file: https://werkzeug.palletsprojects.com/en/2.2.x/datastructures/#werkzeug.datastructures.FileStorage