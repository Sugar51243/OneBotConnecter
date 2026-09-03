from OneBotConnecter.types.message import Message


class AtMessage(Message):

    message_type = "at"

    def __init__(self, qq: str | int):
        if isinstance(qq, int):
            qq = str(qq)
        self.qq = qq
