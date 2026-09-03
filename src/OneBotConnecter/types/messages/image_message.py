
from OneBotConnecter.types.message import Message

class ImageMessage(Message):
    message_type = "image"

    file: str
    summary: str

    def __init__(self,  file: str, summary: str = None):
        self.file = file
        self.summary = summary
