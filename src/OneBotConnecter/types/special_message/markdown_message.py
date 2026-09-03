from OneBotConnecter.types.message import Message


class MarkdownMessage(Message):
    message_type = "markdown"
    can_add_to_chain = False

    def __init__(self, content):
        self.content = content
