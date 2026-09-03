from OneBotConnecter.types.message import Message


class JsonMessage(Message):
    message_type = "json"
    can_add_to_chain = False

    def __init__(self, data):
        self.data = data
