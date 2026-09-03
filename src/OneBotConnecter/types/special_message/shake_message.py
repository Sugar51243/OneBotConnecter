from OneBotConnecter.types.message import Message


class ShakeMessage(Message):
    """窗口抖动（戳一戳）訊息段。"""

    message_type = "shake"
    can_add_to_chain = False
