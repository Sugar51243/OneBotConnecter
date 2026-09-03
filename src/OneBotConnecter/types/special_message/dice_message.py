from OneBotConnecter.types.message import Message


class DiceMessage(Message):
    message_type = "dice"
    can_add_to_chain = False

    def __init__(self, result=None):
        self.result = result
