from OneBotConnecter.types.message import Message


class ReplyMessage(Message):
    message_type = "reply"

    def __init__(self, id):
        self.id = id
