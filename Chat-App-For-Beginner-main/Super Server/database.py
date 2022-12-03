class ChatApp:
    def __init__(self):
        self.authentication = [
            {'username': 'smithdavid0301', 'password': '123456'},
            {'username': 'jackmike0104', 'password': 'mike0123'},
            {'username': 'annabelle2803', 'password': 'Bella2002'},
            {'username': 'britney123', 'password': 'spear456'},
            {'username': 'raythecrayon', 'password': 'ray2802'},
        ]

        self.chatroom = [
            {'id': '101', 'ip': '', 'port': 0, 'name': 'literature1', 'amount': 2,
                'log': [
                    {'username': 'smithdavid0301', 'time': '', 'content': 'Hello'},
                    {'username': 'jackmike0104', 'time': '', 'content': 'Hi'}
                ]},
            {'id': '102', 'ip': '', 'port': 0, 'name': 'assignment', 'amount': 2,
                'log': [

                ]},
            {'id': '103', 'ip': '', 'port': 0, 'name': 'talkshow', 'amount': 4,
                'log': [
                    {'username': 'jackmike0104', 'time': '', 'content': 'Xin chào'}
                ]},
            {'id': '201', 'ip': '', 'port': 0, 'name': 'abc', 'amount': 2,
                'log': [

                ]},
            {'id': '202', 'ip': '', 'port': 0, 'name': 'environment', 'amount': 2,
                'log': [

                ]},
            {'id': '203', 'ip': '', 'port': 0, 'name': 'booking', 'amount': 3,
                'log': [

                ]},
            {'id': '301', 'ip': '', 'port': 0, 'name': 'shipwreck', 'amount': 3,
                'log': [

                ]},
        ]

        self.join = [
            {'username': 'jackmike0104', 'roomid': '101'},
            {'username': 'smithdavid0301', 'roomid': '101'},
            {'username': 'britney123', 'roomid': '102'},
            {'username': 'raythecrayon', 'roomid': '102'},
            {'username': 'britney123', 'roomid': '103'},
            {'username': 'jackmike0104', 'roomid': '103'},
            {'username': 'raythecrayon', 'roomid': '103'},
            {'username': 'smithdavid0301', 'roomid': '103'},
            {'username': 'annabelle2803', 'roomid': '201'},
            {'username': 'smithdavid0301', 'roomid': '201'},
            {'username': 'britney123', 'roomid': '202'},
            {'username': 'raythecrayon', 'roomid': '202'},
            {'username': 'annabelle2803', 'roomid': '203'},
            {'username': 'britney123', 'roomid': '203'},
            {'username': 'jackmike0104', 'roomid': '203'},
            {'username': 'jackmike0104', 'roomid': '301'},
            {'username': 'raythecrayon', 'roomid': '301'},
            {'username': 'smithdavid0301', 'roomid': '301'},
        ]


chatapp = ChatApp()
