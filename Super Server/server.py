import socket
# import pandas as pd
import json
import copy
from thread_module import *
from dbms import dbms

FORMAT = "utf-8"

print('server host', socket.gethostbyname(socket.gethostname()))

SERVER  = {
    "PORT" : 5050,
    "IP" : socket.gethostbyname(socket.gethostname())
}

class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((SERVER["IP"], SERVER["PORT"]))
        self.server.listen(20)

        self.online = {}
        # self.sender_mutex = Lock()
    def listenNewConnection(self):
        print("server is listening")
        while True:
            conn, addr = self.server.accept()
            thread = ThreadWithReturnValue(target=self.listener,args=(conn, addr))
            thread.start()
    def sender(self, content, conns):
        # try:
        for conn in conns:
            # print(content)
            conn.send(content.encode(FORMAT))
        # except:
        #     print('please try again')
    def set_roomchat_ip(self, roomchats, ip):
        pass

    def require_connect(self, rooms):
        packet = {
            "request": "connect",
            "host": (SERVER["IP"], SERVER["PORT"]),
            "data": {
                "connect" : []
            }
        }
        for r in rooms:
            packet["data"]["connect"].append({'ip': r['ip'], 'port': r["port"], 'roomid': r['roomid']})
        return json.dumps(packet) 
    def check_login(self, username, password):
        sign = dbms.checkLogin(username, password)
        packet = {}
        packet["response"] = "signin"
        packet["host"] = (SERVER["IP"], SERVER["PORT"])
        packet["data"] = {}
        if sign: #signin successful
            print("success login")
            packet["data"]["state"] = "success"
            packet["data"]["username"] = username
            packet["data"]["userRooms"] = dbms.selectUserRooms(username)
        else:
            packet["data"]["state"] = "failure"
        packet = json.dumps(packet)
        return sign, packet
    def check_signup(self, username, password):
        pass

    def listener(self, conn, addr):
        connected = True
        # try:
        while connected:
            packet = conn.recv(1024).decode(FORMAT)
            packet = json.loads(packet)

            if "file" in packet:
                print(packet["data"])
                username = packet["author"][0]
                roomid = packet["roomID"]
                user_in_same_room = dbms.getUserFromRoomId(roomid)
                print(username, roomid, user_in_same_room)
                packet= json.dumps(packet)
                for user in user_in_same_room:
                    if user in self.online and user != username: #not resend to owner's message
                        self.sender(packet, [self.online[user]])
                        print('reback')
            else:
                if packet["request"] == "signin":            
                    username = packet["data"]["username"]
                    password = packet["data"]["password"]
                    sign, data = self.check_login(username, password)
                    if sign:
                        self.online[username] = conn
                        # 2 times send near by
                        self.sender(data, [conn])
                        rooms = dbms.setRoomIp(dbms.selectUserRooms(username), packet["host"])
                        if len(rooms) > 0:
                            print("require peer 2 peer")
                            packet = self.require_connect(rooms)
                            self.sender(packet, [conn])
                # elif packet["type"] == "select":
                #     if packet["object"] == "room":
                #         roomid = packet["room"]['id']
                #         username = packet["username"]
                        # self.response_logs(roomid)
                elif packet["request"] == "message":
                    username = packet["data"]["log"]["username"]
                    roomid = packet["data"]["roomid"]
                    newLog = packet["data"]["log"]
                    dbms.pushLog2RoomId(roomid, newLog)
                    log = dbms.getLogFromRoomId(roomid)

                    data = {
                        "roomid": roomid,
                        "log": log
                    }

                    resPacket = {}
                    resPacket["response"] = "message"
                    resPacket["host"] = (SERVER["IP"], SERVER["PORT"])
                    resPacket["data"] = data
                    resPacket = json.dumps(resPacket)
                    user_in_same_room = dbms.getUserFromRoomId(roomid)
                    for user in user_in_same_room:
                        if user in self.online and user != username: #not resend to owner's message
                            self.sender(resPacket, [self.online[user]])
                            print('reback')
        # except :
        #     conn.close()
    
    


server=Server()
server.listenNewConnection()

# sql in pandas https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_sql.html
