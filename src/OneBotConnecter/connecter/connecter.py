from OneBotConnecter.connecter.websocket_connecter import websocket_connecter
from OneBotConnecter.loger.log_info import log, error
from threading import Lock, Thread
import time, uuid

class response_item:

    raw_data: dict

    def __init__(self, data: dict):
        for k, v in data.items():
            if isinstance(k, (list, tuple)):
                setattr(self, k, [response_item(x) if isinstance(x, dict) else x for x in v])
            else:
                setattr(self, k, response_item(v) if isinstance(v, dict) else v)
        self.raw_data = data

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
        # 這些列表屬於目前連線，避免多個 connecter 實例互相共用資料。
        self.temp_list = []
        self.message_list = []
        self.recode_list = []
        self.in_use_echo = []
        self.response_lock = Lock()
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
        if message.get("retcode", None) != None:
            echo = message.get("echo", None)
            with self.response_lock:
                if echo not in self.in_use_echo:
                    log(f"接口回复信息中包含未使用echo参数[{echo}]，正在使用参数为{self.in_use_echo}")
                    return False
                self.recode_list.append(message)
        else:
            self.message_list.append(message)
        log(f"已分类信息: {message}")

    def _wait_for_response(self, echo, timeout=30):
        """等待並取出指定 echo 的接口回覆。"""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            with self.response_lock:
                for index, response in enumerate(self.recode_list):
                    if response.get("echo") == echo:
                        self.recode_list.pop(index)
                        if echo in self.in_use_echo:
                            self.in_use_echo.remove(echo)
                        return response
            time.sleep(0.01)

        with self.response_lock:
            if echo in self.in_use_echo:
                self.in_use_echo.remove(echo)
        raise TimeoutError(f"等待接口回覆超时: echo={echo}")

    def get_message_forever(self):
        thread = Thread(target=(self._get_msg_from_server))
        thread.start()
        return thread

    def send_to_server(self, action: str, body: dict):
        echo = uuid.uuid4().hex
        data = {
            "action": action,
            "params": body,
            "echo": echo
        }
        self.in_use_echo.append(echo)
        log(f"发送数据包: {data}")
        if self.websocket.send_msg_to_server(data):
            try:
                response = self._wait_for_response(echo=echo)
                log(f"接口回复: {response}")
                response = response_item(response)
                return response
            except Exception as e:
                error(e)
        return {}
        