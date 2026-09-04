"""建立合并转发消息。"""

from OneBotConnecter.Event.Message_Event import Message_Event
from OneBotConnecter.OneBot import OneBot
from OneBotConnecter.types import ForwardChain, NodeMessage


WS_URL = "ws://127.0.0.1:3001"


def on_message(bot, message: Message_Event):
    if message.raw_message != "forward":
        return

    forward = ForwardChain(
        [
            NodeMessage(name="机器人", uin=message.user_id, content=["第一条转发消息"]),
            NodeMessage(name="机器人", uin=message.user_id, content=["第二条转发消息"]),
        ],
        summary="示例转发",
        prompt="查看合并转发内容",
    )
    message.reply_message(forward)


if __name__ == "__main__":
    OneBot(WS_URL, on_message).run()