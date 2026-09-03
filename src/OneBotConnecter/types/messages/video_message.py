
from OneBotConnecter.types.message import Message

class VideoMessage(Message):
    message_type = "video"
    can_add_to_chain = False

    file: str

    def __init__(self, file: str):
        self.file = file