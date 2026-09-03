from OneBotConnecter.connecter.websocket_connecter import websocket_connecter
from OneBotConnecter.loger.log_info import log, error
from threading import Thread
import time


class connecter:

    url: str
    websocket: websocket_connecter

    temp_list: list = []
    message_list: list = []
    recode_list: list = []
    in_use_echo: list = []

    connection_status = False
    keep_running = True

    def __init__(self, url: str):
        log("连接器正在初始化")
        self.url = url
        self.websocket = websocket_connecter(url)
        self.connection_status = True
        log("连接器初始化完成")

    def _get_msg_from_server(self):
        while self.keep_running:
            message = self.websocket.get_msg_from_server()
            if message.get("meta_event_type", "") == "heartbeat":
                bot_status = message.get("status", {}).get("online", False)
                if bot_status != self.connection_status:
                    log(f"账号连接状态变为: {bot_status}")
                self.connection_status = bot_status
            self._classify_message(message)
            time.sleep(1)
        print("信息获取线程已关闭")

    def _classify_message(self, message):
        if not message or message.get("meta_event_type", "") == "heartbeat":
            return False
        if message.get("retcode", None):
            echo = message.get("echo", None)
            if echo not in self.in_use_echo:
                log(f"接口回复信息中包含未使用echo参数[{echo}]，正在使用参数为{self.in_use_echo}")
                return False
            self.in_use_echo.remove(echo)
            self.recode_list.append(message)
        else:
            self.message_list.append(message)
        log(f"已分类信息: {message}")

    def get_message_forever(self):
        thread = Thread(target=(self._get_msg_from_server))
        thread.start()
        return thread