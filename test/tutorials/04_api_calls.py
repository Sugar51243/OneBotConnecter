"""在回呼中调用查询接口和主动发送接口。

账号属性教程请参考 06_account_info.py。
"""

from OneBotConnecter.Event.Message_Event import Message_Event
from OneBotConnecter.OneBot import OneBot


WS_URL = "ws://127.0.0.1:3001"


def on_message(bot, message: Message_Event):
    if message.raw_message == "info":
        login = bot.get_login_info()
        message.reply_message(f"登录信息：{login.data.nickname} ({login.data.user_id})")
    elif message.raw_message == "send" and message.raw_data.get("group_id"):
        bot.send_group_msg(message.group_id, "这是通过 bot API 主动发送的消息")


if __name__ == "__main__":
    OneBot(WS_URL, on_message).run()