import socket
from queue import Queue
import json
import copy
import time
import copy
from python.thread_module import ThreadWithReturnValue


SERVER  = {
    "PORT" : 5050,
    "IP" : socket.gethostbyname(socket.gethostname())
}

FORMAT = "utf-8"

class User:
    def __init__(self):
        self.host = (socket.gethostbyname(socket.gethostname()), 6001)
        self.login = [False]
        # self.queue_packet = Queue(0)
        self.userRoomsData = []
        self.username = [""]
        self.currentRoomId = [""]
        self.online = {}

        #for file, please don't delete
        self.author=[]
        self.file=[]
        self.state_file=[]

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client.bind(self.host)
        self.client.listen(10)
        
        self.exist = True 
        thread_client = ThreadWithReturnValue(target=self.listenNewConnection)

        thread_client.start()

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((SERVER["IP"], SERVER["PORT"]))

        thread_server = ThreadWithReturnValue(target=self.listener, args=(self.server, (SERVER["IP"], SERVER["PORT"])))
        thread_server.start()

    def listenNewConnection(self):
        # print("server is listening")
        # COUNT[0] +=1
        # print(COUNT[0])
        while not self.login[0]:
            time.sleep(2)
            print("user not login")
        while True:
            print("user is waiting new connection")
            conn, addr = self.client.accept()
            print("new client connect", addr)
            thread = ThreadWithReturnValue(target=self.listener,args=(conn, addr))
            thread.start()
    def getRoomById(self, roomID):
        for r in self.userRoomsData:
            if r['id'] == roomID:
                return r
        return None
    def send_message(self, message):
        print('test1', self.userRoomsData)
        if message == "":
            return
        room = self.getRoomById(self.currentRoomId[0])
        if room is None:
            return
        packet = {
            "request": "message",
            "host": self.host,
            "data": {                
                "roomid": self.currentRoomId[0],
                "log":{
                    "username": self.username[0],
                    "content": message,
                    "time": ""
                }
            }
        }
        # self append message to self log
        self.getRoomById(self.currentRoomId[0])["log"].append(packet["data"]["log"])
        packet = json.dumps(packet)
        if room["amount"] > 2:
            print("send to server")
            self.sender(packet, [self.server])
        else:
            if self.currentRoomId[0] in self.online:
                try:
                    self.online[self.currentRoomId[0]].send(packet.encode(FORMAT))
                except:
                    print("user not online")
            else:
                print("user not online")
                print(self.online)
    def selectChatRoom(self, roomIDSelected):
        # packet = copy.deepcopy(JSON_TEMPLATE["request"]["select_room"])
        # packet["room"] = copy.deepcopy(JSON_TEMPLATE["room"])
        # packet["room"]["id"] = roomIDSelected
        # packet = json.dumps(packet)
        # self.sender(packet, [self.server])        
        pass
    def sender(self, packet, conns):
        # try:
        for conn in conns:
            conn.send(packet.encode(FORMAT))
        # except:
        #     print('please try again')

    def syncLog(self, roomid, log):
        for r in self.userRoomsData:
            if r["id"] == roomid:
                r["log"] = log
        print("done")

    def listener(self, conn, addr):
        try:
            while True:
                packet = conn.recv(1024).decode(FORMAT)
                packet = json.loads(packet) 
                if "file" in packet:
                    #ID:sender:filename
                    print(packet)
                    sender_file=packet["roomID"]+":"+packet["author"]+":"+packet["file"]
                    cur_idx=-1
                    print(sender_file)
                    if sender_file in self.author:
                        index = len(self.author) - 1 - self.author[::-1].index(sender_file)
                        if(self.state_file[index]=="Finished"):
                            self.author.append(sender_file)
                            self.file.append(packet["data"])
                            self.state_file.append(packet["state"])
                            cur_idx=len(self.file)-1
                        else:
                            self.file[index]=self.file[index]+packet["data"]
                            if(packet["state"]!="Finished"):
                                self.file[index]=self.file[index]+"|"
                            self.state_file[index]=packet["state"]
                            cur_idx=index
                    else:
                        self.author.append(sender_file)
                        self.file.append(packet["data"])
                        self.state_file.append(packet["state"])
                        cur_idx=0
                    if(packet["state"]=="Finished"):
                        print(self.file[cur_idx])
                        print("End of file")
                        self.save_file(packet["file"],cur_idx)

                        mess = {}
                        mess["data"] = {
                            "log":{
                                "username":packet["author"],
                                "content":"file",
                                'time': '',
                                "file": packet["file"]
                            }
                        }              
                        self.getRoomById(packet["roomID"])["log"].append(mess["data"]["log"])
                        print(mess)

                else:
                    if packet["host"][0] == SERVER["IP"] and packet["host"][1] ==  SERVER["PORT"]:
                        if "response" in packet:
                            if packet["response"] == 'signin':
                                if packet["data"]["state"] == 'success':
                                    self.username[0] = packet["data"]["username"]
                                    self.userRoomsData = copy.deepcopy(packet["data"]["userRooms"])
                                    self.login[0] = True
                                    # print(self.userRoomsData)
                                else:
                                    self.login[0] = False
                                    print('self.login[0]', False)
                            if packet["response"] == 'message':
                                roomid, log = packet["data"]["roomid"], packet["data"]["log"]
                                self.syncLog(roomid, log)
                            if packet["response"] == "signup":
                                if( packet["data"]["state"]=="Success"):
                                    self.exist = False
                                
                        elif "request" in packet:
                            if packet["request"] == "connect":
                                for con in packet["data"]["connect"]:
                                    newConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                    print(con)
                                    newConn.connect((con["ip"], con["port"]))
                                    sentUsername = False
                                    t_end = time.time() + 2 # 2s response
                                    while sentUsername == False and time.time() < t_end:
                                        try:
                                            # user require to connect
                                            newPacket = {
                                                "request": "connect",
                                                "host": self.host,
                                                "data":{
                                                    "username": self.username[0],
                                                    "roomid": con["roomid"]
                                                }
                                            }
                                            newPacket = json.dumps(newPacket)
                                            newConn.send(newPacket.encode(FORMAT))
                                            sentUsername = True
                                        except:
                                            pass
                                    if sentUsername:
                                        # client connect to client hold socket
                                        self.online[con["roomid"]] = newConn
                                        print('sent username success', self.online)
                                        thread = ThreadWithReturnValue(target=self.listener, args=(newConn, (con["ip"], con["port"])))
                                        thread.start()
                                    else:
                                        print('can not connect peer2peer')
                    else:
                        # listen user require to connect
                        if "request" in packet:
                            if packet["request"] == "connect":
                                # client listen to client hold socket
                                self.online[packet["data"]["roomid"]] = conn
                                print('self online', self.online)
                                print(packet["data"]["roomid"], conn)
                                print('self.userRoomsData', self.userRoomsData)
                            if packet["request"] == "message":
                                print('step 2')
                                print('userRoomsData', self.userRoomsData)
                                r = self.getRoomById(packet["data"]["roomid"])
                                print(r)
                                print(r["log"])
                                print(packet["data"]["log"])
                                r["log"].append(packet["data"]["log"])

        except:
            print("your friend have loged out")
            conn.close()
            return
    def save_file(self, file_name, index):
        temp_data=self.file[index].split('|')
        file = open(file_name,'a+')
        for i in temp_data:
            file.write(i)

    def get_login_status(self):
        return self.login[0]
    def requestSignin(self, username, password):
        packet = {}
        packet["request"] = "signin"
        packet["host"] = self.host
        packet["data"] = {}
        packet["data"]["username"] = username
        packet["data"]["password"] = password
        packet = json.dumps(packet)
        self.sender(packet, [self.server])
        return self.wait_for_login()
    def wait_for_login(self):
        is_login = self.get_login_status()
        t_end = time.time() + 2 # 2s response
        while is_login == False and time.time() < t_end:
            is_login = self.get_login_status()
        return is_login
    
    def wait_for_signup(self):
        is_exist= self.exist
        t_end = time.time() + 5 # 5s response
        while is_exist == True and time.time() < t_end:
            is_exist = self.exist
        return is_exist
    def request_signup(self,name,username,password,gender):
        packet ={}
        packet["request"] = "signup"
        packet["host"] = self.host
        packet["data"] = {}
        packet["data"]["username"] = username
        packet["data"]["password"] = password
        packet = json.dumps(packet)
        print(packet)
        self.sender(packet, [self.server])
        return not self.wait_for_signup()
    
    def send_file(self, fileMessage):
        file_name = fileMessage.filename
        # path= path + file_name
        # file_read = open(path,"r")
        room = self.getRoomById(self.currentRoomId[0])
        
        # file_read = fileMessage.stream
        upload = fileMessage.read(500).decode('latin')
        # upload=file_read.read(500)
        while upload :
            mess = {}
            mess["file"]=file_name
            mess["author"]=self.username[0]
            mess["roomID"]= self.currentRoomId[0]
            mess["data"]=upload
            # upload=file_read.read(500)
            upload = fileMessage.read(500).decode('latin')
            if(upload==""):
                mess["state"]="Finished"
            else:
                mess["state"]="NOT YET"
            print(mess)
            mess = json.dumps(mess)
            # print(mess)
            if room["amount"] > 2:
                print("send to server")
                self.sender(mess, [self.server])
            else:
                if self.currentRoomId[0] in self.online:
                    self.online[self.currentRoomId[0]].send(mess.encode(FORMAT))
            print('----')
        packet={}
        packet["data"]={
            "log":{
                "username":self.username[0],
                "content":"file",
                'time': '',
                "file": file_name
            }
        }
        self.getRoomById(self.currentRoomId[0])["log"].append(packet["data"]["log"])
        print(packet)
        # file_read.close()
Client = User()