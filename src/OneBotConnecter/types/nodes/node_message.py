
from OneBotConnecter.types.message import Message


class NodeMessage(Message):
    """合并转发节点訊息段，支援 ID 節點與自定義節點。"""

    message_type = "node"
    can_add_to_chain = False

    def __init__(self, id: int=None, name: str=None, uin: int=None, content: list=None, time: int = None, seq: int = None):
        self.id = id
        self.name = name
        self.uin = uin
        self.content = content
        self.time = time
        self.seq = seq
