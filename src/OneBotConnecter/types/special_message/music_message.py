from OneBotConnecter.types.message import Message


class MusicMessage(Message):
    """音乐分享訊息段，支援標準與 custom 格式。"""

    message_type = "music"
    can_add_to_chain = False

    def __init__(self, type, id=None, url=None, audio=None, title=None, image=None):
        self.type = type
        if type == "custom":
            self.url = url
            self.audio = audio
            self.title = title
            self.image = image
        else: self.id = id
