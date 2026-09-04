"""最小可用案例：根据文字内容回复。"""

from OneBotConnecter.Event.Message_Event import Message_Event
from OneBotConnecter.OneBot import OneBot


WS_URL = "ws://127.0.0.1:3001"


def on_message(bot, message: Message_Event):
    try:
        if message.raw_message == "test":
            message.reply_message("hello")
        elif message.raw_message == "ping":
            message.reply_message("pong")
    except Exception:
        # 记录无法识别的事件，避免单个事件中断回呼线程。
        print(message.raw_data)


if __name__ == "__main__":
    OneBot(WS_URL, on_message).run()