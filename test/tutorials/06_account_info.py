"""从回呼函数的 bot 参数取得 OneBot 账号信息。"""

from OneBotConnecter.Event.Message_Event import Message_Event
from OneBotConnecter.OneBot import OneBot


WS_URL = "ws://127.0.0.1:3001"


def on_message(bot, message: Message_Event):
    if message.raw_message != "account":
        return

    # 回呼参数 bot 是 message_interface，OneBot 实例位于 bot.bot。
    account = bot.bot
    account_id = account.user_id
    nickname = account.nickname
    owners = account.owner

    message.reply_message(
        f"账号：{nickname} ({account_id})\n"
        f"管理员：{owners}"
    )


if __name__ == "__main__":
    OneBot(WS_URL, on_message, owner=[123456]).run()