from OneBotConnecter.types.message import Message
import random


class DiceMessage(Message):
    message_type = "dice"
    can_add_to_chain = False

    def __init__(self, result=None):
        if result == None:
            result = random.randint(1,6)
        self.result = result
