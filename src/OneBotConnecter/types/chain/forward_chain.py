
from OneBotConnecter.types.message import Message
from OneBotConnecter.loger.log_info import error
from OneBotConnecter.types.messages.text_message import TextMessage
from OneBotConnecter.types.nodes.node_message import NodeMessage
from OneBotConnecter.types.chain.message_chain import MessageChain

class ForwardChain(Message):

    message: list = []
    can_add_to_chain = False

    def __init__(self, message, source: str = None, news: list = [], summary: str = None, prompt: str = None):
        self.message = []
        self.add(message=message)
        self.source = source
        if len(news)<1 or len(news)>4:
            error(f"预览文本数量({len(news)})不符合需求")
            news = []
        self.news = []
        for new in news:
            if not isinstance(new, str):
                error(f"预览文本并非字符串: {new}")
                continue
            self.news.append(new)
        if len(self.news) <= 0: self.news = None
        self.summary = summary
        self.prompt = prompt

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
            message = TextMessage(message)
            nodes = NodeMessage(content=[message])
            temp.append(nodes)
        elif isinstance(message, list):
            for item in message:
                temp.extend(self._non_message_to_message(item))
        elif isinstance(message, ForwardChain):
            temp = message.message
        elif isinstance(message, NodeMessage):
            temp.append(message)
        elif isinstance(message, MessageChain):
            message = message.message
            for item in message:
                temp.extend(self._non_message_to_message(item))
        elif isinstance(message, Message):
            nodes = NodeMessage(content=[message])
            temp.append(nodes)
        else:
            error(f"该种类不可加入信息链({type(message)}): {message}")
        return temp

    def to_send_message(self):
        data = []
        for message in self.message:
            data.append(message.to_send_message())
        data = {
            "messages": data,
            "source": self.source,
            "news": self.news,
            "summary": self.summary,
            "prompt": self.prompt
        }
        return data