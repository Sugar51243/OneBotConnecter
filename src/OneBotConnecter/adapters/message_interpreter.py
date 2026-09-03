

from __future__ import annotations

from OneBotConnecter.loger.log_info import error


class message_interpreter:

    def __init__(self):
        self.message_types = self._load_message_types()

    def _load_message_types(self):
        from OneBotConnecter.types import (
            AtMessage,
            DiceMessage,
            FaceMessage,
            ImageMessage,
            JsonMessage,
            MarkdownMessage,
            MusicMessage,
            NodeMessage,
            RecordMessage,
            ReplyMessage,
            RpsMessage,
            ShakeMessage,
            TextMessage,
            VideoMessage,
        )

        return {
            "text": TextMessage,
            "image": ImageMessage,
            "video": VideoMessage,
            "record": RecordMessage,
            "at": AtMessage,
            "reply": ReplyMessage,
            "json": JsonMessage,
            "face": FaceMessage,
            "markdown": MarkdownMessage,
            "node": NodeMessage,
            "music": MusicMessage,
            "dice": DiceMessage,
            "rps": RpsMessage,
            "shake": ShakeMessage,
        }

    def interface_message_to_local_message(self, message: dict, handler):
        from OneBotConnecter.Event.Message_Event import Message_Event

        return Message_Event(message, handler)

    def message_class(self, message: dict):
        message_type = message.get("type")
        message_class = self.message_types.get(message_type)
        if not message_class:
            error(f"信息种类识别失败: {message}")
            return None
        return message_class(**message.get("data", {}))