from OneBotConnecter.types.message import Message


class RpsMessage(Message):
    message_type = "rps"
    can_add_to_chain = False

    def __init__(self, result=None):
        self.result = result
