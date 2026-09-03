

from OneBotConnecter.types.messages.text_message import TextMessage
from OneBotConnecter.types.message import Message
from OneBotConnecter.loger.log_info import error


class MessageChain(Message):
    """由多個 OneBot 訊息段組成的訊息鏈。"""

    message: list

    def __init__(self, message):
        self.message = []
        self.add(message=message)

    def __add__(self, other):
        self.add(message=other)
        return self

    def add(self, message):
        message = self._non_message_to_message(message)
        self.message.extend(message)
        return self

    def _non_message_to_message(self, message):
        temp = []
        if isinstance(message, str):
            temp.append(TextMessage(message))
        elif isinstance(message, list):
            for item in message:
                temp.extend(self._non_message_to_message(item))
        elif isinstance(message, MessageChain):
            temp = message.message
        elif isinstance(message, Message):
            if not message.can_add_to_chain:
                raise TypeError(
                    f"{type(message).__name__} 不可加入 MessageChain，"
                    "請單獨建立並依接口要求發送"
                )
            temp.append(message)
        else:
            error(f"该种类不可加入信息链({type(message)}): {message}")
        return temp

    @property
    def text(self):
        """取得訊息鏈中所有文字段合併後的內容。"""
        return "".join(item.text for item in self.message if isinstance(item, TextMessage))

    @property
    def texts(self):
        """取得訊息鏈中所有文字段內容。"""
        return [item.text for item in self.message if isinstance(item, TextMessage)]

    def get(self, message_type):
        """取得指定類型的訊息段。"""
        return [item for item in self.message if getattr(item, "message_type", None) == message_type]

    def to_send_message(self):
        data = []
        for message in self.message:
            data.append(message.to_send_message())
        return data