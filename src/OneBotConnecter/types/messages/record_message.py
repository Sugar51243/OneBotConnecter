from OneBotConnecter.types.message import Message


class RecordMessage(Message):
    message_type = "record"
    can_add_to_chain = False

    def __init__(self, file, url=None, path=None, file_size=None, thumb=None, name=None):
        self.file = file
        self.url = url
        self.path = path
        self.file_size = file_size
        self.thumb = thumb
        self.name = name
