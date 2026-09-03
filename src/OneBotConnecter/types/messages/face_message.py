from OneBotConnecter.types.message import Message


class FaceMessage(Message):
    message_type = "face"

    def __init__(self, id):
        self.id = id
