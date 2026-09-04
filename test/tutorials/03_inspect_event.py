"""读取事件字段，并解析收到的消息段。"""

from OneBotConnecter.Event.Message_Event import Message_Event
from OneBotConnecter.OneBot import OneBot


WS_URL = "ws://127.0.0.1:3001"


def on_message(bot, message: Message_Event):
    if message.raw_message == "inspect":
        print("event_type:", message.event_type)
        print("raw_data:", message.raw_data)
        parsed = message.to_send_message()
        if parsed is not None:
            print("text:", getattr(parsed, "text", ""))
            print("text segments:", getattr(parsed, "texts", []))
            print("image segments:", parsed.get("image"))


if __name__ == "__main__":
    OneBot(WS_URL, on_message).run()