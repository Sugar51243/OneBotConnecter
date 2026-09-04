from OneBotConnecter.connecter.connecter import connecter
from OneBotConnecter.adapters.message_interpreter import message_interpreter
from OneBotConnecter.message_handler.message_handler import message_handler
from OneBotConnecter.loger.log_info import print, log, warning
import time


class OneBot:

    url: str
    interface: connecter
    adapter: message_interpreter
    handler: message_handler

    user_id: int
    nickname: str

    owner:list

    threading_list: list = []

    def __init__(self, url, call_function, owner=[]):
        self.url = url
        self.interface = connecter(url)
        self.adapter = message_interpreter()
        self.handler = message_handler(self.interface, self.adapter, call_function, self)
        self.owner = owner
        print("接口已就绪")

    def check_threadings(self):
        self.threading_list = [t for t in self.threading_list if t.is_alive()]
        return len(self.threading_list)

    def run(self):
        self.threading_list.append(self.interface.get_message_forever())
        self.threading_list.append(self.handler.handle_messgae_forever())
        try:
            data = self.handler.handler.get_login_info()
            self.user_id = data.data.user_id
            log(f"USER ID: {self.user_id}")
            self.nickname = data.data.nickname
            log(f"Nickname: {self.nickname}")
        except:
            warning("账号状态获取失败")
        while self.check_threadings() > 0:
            try:
                time.sleep(1)
            except:
                self.interface.keep_running = False
                self.handler.keep_running = False
        print("程序已结束")