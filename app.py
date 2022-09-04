
# from socket import AF_X25
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import datetime
import os
import sys
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")


activeUser = 1

# On connect Event
@socketio.on('connect')
def connect():
    try:
        global activeUser
        print("connected: ", activeUser)
        # Read
        activeUser +=1
        counter = {"counter": activeUser}
        emit("user", counter, broadcast = True)
    except:
        emit("user", {"counter": 0}, broadcast = True)

        
# On Disconnect Event
@socketio.on('disconnect')
def disconnect():
    global activeUser
    print("disconnect: ", activeUser)
    activeUser-=1
    counter = {"counter": activeUser}
    emit("user", counter, broadcast = True)

@app.route("/", methods = ['GET', "POST"])
def home():
    
    global activeUser
    
    respond = {}
    if request.method=="POST":
        data=request.form.getlist('option')[0]
        if data == 'currentServerTimeStamp':
            timeStamp = datetime.datetime.now()
            respond['data']="Current server timestamp:- " + str(timeStamp)
        
        elif data == 'activeClients':
            respond['data']="Active clients:- " + str(activeUser)
        
        elif data == 'connectedTime':
            timeStamp = datetime.datetime.now() - datetime.timedelta(seconds=20)
            respond['data']="connectedTime:- " + str(timeStamp)  
    print(respond)
    return render_template("main.html", data = respond)

if __name__ == '__main__':
    socketio.run(app)