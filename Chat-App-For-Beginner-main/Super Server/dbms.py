from database import chatapp
import copy

class DBMS:
    def __init__(self):
        pass
    def checkLogin(self, username, password):
        for d in chatapp.authentication:
            if d['username'] == username and d['password'] == password:
                return True
        return False
    def selectUsersInRoomId(self, roomid):
        users = []
        for d in chatapp.join:
            if d["roomid"] == roomid:
                users.append(d["username"])
        return users

    def selectUserRooms(self, username):
        listRoomID = []
        for d in chatapp.join:
            if d['username'] == username:
                listRoomID.append(copy.deepcopy(d['roomid']))
        # print(listRoomID)
        userRooms = []
        for d in chatapp.chatroom:
            if d['id'] in listRoomID:
                room = copy.deepcopy(d)
                userRooms.append(room)
        # print(userRooms)
        return userRooms  
    def pushLog2RoomId(self, roomid, log):
        for d in chatapp.chatroom:
            if d['id'] == roomid:
                d['log'].append(log)
                print(d)        
                break
    def getLogFromRoomId(self, roomid):
        for d in chatapp.chatroom:
            if d['id'] == roomid:
                return d['log']
    def getUserFromRoomId(self, roomid):
        users = []
        for j in chatapp.join:
            if j['roomid'] == roomid:
                users.append(j['username'])
        return users
    def getRoomByRoomId(self, roomid):
        for d in chatapp.chatroom:
            if d['id'] == roomid:
                return d
    def setRoomIp(self, userRooms, ip_port):
        rooms = []
        thresh = 5
        for d in userRooms:
            if d['amount'] == 2:
                if thresh > 0 and d['ip'] == '':
                    room = self.getRoomByRoomId(d['id'])
                    room["ip"] = ip_port[0]
                    room["port"] = int(ip_port[1])
                    thresh -= 1
                else:
                    rooms.append({"ip": copy.deepcopy(d['ip']), "roomid": copy.deepcopy(d['id']), "port": d["port"]})
        return rooms

dbms = DBMS()