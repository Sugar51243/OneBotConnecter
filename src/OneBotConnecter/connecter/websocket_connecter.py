from websockets.sync.client import ClientConnection, connect
from OneBotConnecter.loger.log_info import log, error
import time, json



class websocket_connecter:

    url: str
    websocket: ClientConnection


    def __init__(self, url):
        log("正在尝试连接服务器")
        self.url = url
        self._get_connection()
        log("连接已成功")

    def _start_connection(self):
        try:
            self.websocket = connect(self.url)
            self.websocket.recv()
            return True
        except Exception as e:
            error(e)
        return False

    def _get_connection(self):
        try:
            self.websocket.close()
        except: pass
        while not self._start_connection():
            time.sleep(5)
        return True

    def get_msg_from_server(self):
        try:
            msg = self.websocket.recv()
            msg = json.loads(msg)
            return msg
        except Exception as e:
            error(e)
            self._get_connection()
            return {}

    def send_msg_to_server(self, msg):
        try:
            self.websocket.send(msg)
            return True
        except Exception as e:
            error(e)
            self._get_connection()
            return False