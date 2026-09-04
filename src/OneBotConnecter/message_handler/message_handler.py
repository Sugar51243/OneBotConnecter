from OneBotConnecter.connecter.connecter import connecter
from OneBotConnecter.adapters.message_interpreter import message_interpreter
from OneBotConnecter.message_handler.message_interface import message_interface
from OneBotConnecter.loger.log_info import log, error
from threading import Thread
import time

class message_handler:

    inface: connecter
    adapter: message_interpreter
    callback_function: __module__
    handler: message_interface
    keep_running = True

    def __init__(self, inface: connecter, adapter: message_interpreter, call_function: __module__, bot):
        log("信息处理器正在初始化")
        self.inface = inface
        self.adapter = adapter
        self.handler = message_interface(inface, adapter)
        self.bot = bot
        self.callback_function = call_function
        log("信息处理器初始化完成")

    def _handle_message(self):
        while self.keep_running:
            if len(self.inface.message_list) <= 0:
                time.sleep(1)
                continue
            try:
                raw_message = self.inface.message_list.pop(0)
                while self.bot.check_threadings() >= 15:
                    time.sleep(1)
                thread = self._run_callback_function(raw_message)
                self.bot.threading_list.append(thread)
            except Exception as e:
                error(e)
            time.sleep(1)
        print("信息处理线程已关闭")

    def _run_callback_function(self, raw_message):
        def call_function():
            message = self.adapter.interface_message_to_local_message(message=raw_message, handler=self.handler)
            try:
                self.callback_function(bot=self.handler, message=message)
            except Exception as e:
                error(e)
            log(f"已处理信息: {raw_message}")
        thread = Thread(target=call_function)
        thread.start()
        return thread

    def handle_messgae_forever(self):
        thread = Thread(target=self._handle_message)
        thread.start()
        return thread