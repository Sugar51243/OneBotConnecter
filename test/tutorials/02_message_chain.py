"""建立包含文字、At 和图片的 OneBot 消息链。"""

from OneBotConnecter.Event.Message_Event import Message_Event
from OneBotConnecter.OneBot import OneBot
from OneBotConnecter.types import AtMessage, ImageMessage, MessageChain, TextMessage


WS_URL = "ws://127.0.0.1:3001"


def on_message(bot, message: Message_Event):
    if message.raw_message == "chain":
        chain = MessageChain([
            TextMessage("你好，"),
            AtMessage(message.user_id),
            TextMessage(" 这是组合消息。"),
            ImageMessage("https://example.com/image.png"),
        ])
        message.reply_message(chain)


if __name__ == "__main__":
    OneBot(WS_URL, on_message).run()