
from OneBotConnecter.types.message import Message

class TextMessage(Message):
    message_type = "text"

    text: str

    def __init__(self, text: str):
        self.text = text