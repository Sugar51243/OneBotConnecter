from abc import ABC, abstractmethod
import random
from typing import Literal

#抽象类: 信息(发送)
class Message(ABC):
    def __init__(self): pass
    @abstractmethod
    def to_dict(self): return {}
    @abstractmethod
    def returnData(self): return []

# 文字信息
class TextMessage(Message):

    text = ""

    def __init__(self, data: str):
        if len(data) > 10000:
            raise ValueError("内容过长")
        self.text = data
    
    def to_dict(self):
        msg = {
            "type": "text",
            "data": {
                "text": self.text
            }
        }
        return msg

    def returnData(self):
        return [self]
    
# 回复信息
class ReplyMessage(Message):

    message_id: int

    def __init__(self, message_id: int):
        self.message_id = message_id
    
    def to_dict(self):
        msg = {
            "type": "reply",
            "data": {
                "id": self.message_id
            }
        }
        return msg

    def returnData(self):
        return [self]
    
# 图片信息
class ImageMessage(Message):

    data: str

    def __init__(self,  data: str):
        self.data = data
    
    def to_dict(self):
        msg = {
            "type": "image",
            "data": {
                "file": self.data
            }
        }
        return msg

    def returnData(self):
        return [self]
    
# 表情信息
class EmojiMessage(Message):

    data: str

    def __init__(self,  id: str):
        self.id = id
    
    def to_dict(self):
        msg = {
            "type": "face",
            "data": {
                "id": self.id
            }
        }
        return msg

    def returnData(self):
        return [self]
    
# 语音信息
class RecordMessage(Message):

    data: str

    def __init__(self,  data: str):
        self.data = data
    
    def to_dict(self):
        msg = {
            "type": "record",
            "data": {
                "file": self.data
            }
        }
        return msg

    def returnData(self):
        return [self]
    
# 视频信息
class VideoMessage(Message):

    data: str

    def __init__(self,  data: str):
        self.data = data
    
    def to_dict(self):
        msg = {
            "type": "video",
            "data": {
                "file": self.data
            }
        }
        return msg

    def returnData(self):
        return [self]
    
# 超级表情: 骰子信息
class DiceMessage(Message):

    result: int

    def __init__(self, result: int = None):
        self.result = result
    
    def to_dict(self):
        if self.result == None:
            self.result = random.randint(1,6)
        msg = {
            "type": "dice",
            "data": {
                "result": self.result
            }
        }
        return msg

    def returnData(self):
        return [self]
    
# 超级表情: 猜拳信息
class RPSMessage(Message):

    def __init__(self): pass
    
    def to_dict(self):
        msg = {
            "type": "rps",
            "data": {}
        }
        return msg

    def returnData(self):
        return [self]
    
# QQ音乐卡片信息
class QQMusicMessage(Message):

    id: int

    def __init__(self, id: int):
        self.id = id
    
    def to_dict(self):
        msg = {
            "type": "music",
            "data": {
                "type": "qq",
                "id": self.id
            }
        }
        return msg

    def returnData(self):
        return [self]
    
# 网易云音乐卡片信息
class Music163Message(Message):

    id: int

    def __init__(self, id: int):
        self.id = id
    
    def to_dict(self):
        msg = {
            "type": "music",
            "data": {
                "type": "163",
                "id": self.id
            }
        }
        return msg

    def returnData(self):
        return [self]
    
# 自定义音乐卡片信息
class CustomMusicMessage(Message):

    url: str
    audio: str
    title: str
    image: str

    def __init__(self, url: str, audio: str, title: str, image: str):
        self.url = url
        self.audio = audio
        self.title = title
        self.image = image
    
    def to_dict(self):
        msg = {
            "type": "music",
            "data": {
                "type": "custom",
                "audio": self.url,
                "audio": self.audio,
                "title": self.title,
                "image": self.image
            }
        }
        return msg

    def returnData(self):
        return [self]
    
# 卡片信息
class PrivateCardMessage(Message):

    data: str

    def __init__(self, data: str):
        self.data = data
    
    def to_dict(self):
        msg = {
            "type": "json",
            "data": {
                "data": self.data
            }
        }
        return msg

    def returnData(self):
        return [self]


class Nodes:

    data: list[Message]
    user_id: str
    nickname: str
    isGroup: bool

    def __init__(self, data: list[Message] | Message, user_id: str = None, nickname: str = None, isGroup = True):
        if isinstance(data, MessageChain):
            data = data.returnData()
        elif not isinstance(data, list):
            data = [data]
        self.data = data
        self.user_id = user_id
        self.nickname = nickname
        self.isGroup = isGroup
    
    def _to_node(self, content):
        if self.isGroup:
            msg = {
                "type": "node",
                "data": {
                    "uin": self.user_id,
                    "name": self.nickname,
                    "content": content
                }
            }
        else:
            msg = {
                "type": "node",
                "data": {
                    "content": content
                }
            }
        return msg

    def to_dict(self):
        return_data = []
        temp = []
        for msg in self.data:
            if isinstance(msg, ImageMessage):
                if temp: return_data.append(self._to_node(temp))
                temp = []
                return_data.append(self._to_node([msg.to_dict()]))
                continue
            temp.append(msg.to_dict())
        if len(temp)>0:
            return_data.append(self._to_node(temp))
        return return_data

    def returnData(self):
        return [self]

# 合并转发信息
class ForwardMessage(Message):

    notes: list[Nodes]

    def __init__(self, data: list[Message] | list[Nodes] | Message, user_id: str = None, nickname: str = None, isGroup = True):
        if isinstance(data, list):
            if isinstance(data[0], Nodes):
                self.notes = data
                return
        note = Nodes(data = data, user_id = user_id, nickname = nickname, isGroup = isGroup)
        self.notes= note.returnData()

    def add_notes(self, data: list[Message] | list[Nodes] | Message | Nodes, user_id: str = None, nickname: str = None, isGroup = True):
        if isinstance(data, list):
            if isinstance(data[0], Nodes):
                self.notes.extend(data)
                return
            for msg in data:
                if isinstance(data[0], ForwardMessage):
                    self.notes.extend(data[0].notes)
            return
        if isinstance(data, Nodes):
            self.notes.extend([data])
            return
        elif isinstance(data, ForwardMessage):
            self.notes.extend(data.notes)
            return
        note = Nodes(data = data, user_id = user_id, nickname = nickname, isGroup = isGroup)
        self.notes.extend([note])
    
    def to_dict(self):
        return_data = []
        for n in self.notes:
            return_data.extend(n.to_dict())
        return return_data

    def returnData(self):
        return [self]
    
# @信息
class AtMessage(Message):

    qq: str

    def __init__(self, qq: int | Literal["all"]):
        if type(qq) == int:
            qq = str(qq)
        self.qq = qq
    
    def to_dict(self):
        msg = {
            "type": "at",
            "data": {
                "qq": self.qq
            }
        }
        return msg

    def returnData(self):
        return [self]
    
# 信息链
class MessageChain(Message):
    
    data: list[Message]

    def __init__(self, data: list[Message|str] = []):
        temp = []
        for msg in data:
            if type(msg) == str:
                msg = TextMessage(msg)
            temp.append(msg)
        self.data = temp

    def add(self, message):
        if type(message) == str:
            message = TextMessage(message)
        self.data.extend(message.returnData())
    
    def to_dict(self):
        return [msg.to_dict() for msg in self.data]

    def returnData(self):
        return self.data
