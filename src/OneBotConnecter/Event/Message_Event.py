
from __future__ import annotations

from typing import TYPE_CHECKING

from OneBotConnecter.types.message import Message
from OneBotConnecter.types import AtMessage, ReplyMessage, MessageChain, ForwardChain, NodeMessage

if TYPE_CHECKING:
    from OneBotConnecter.message_handler.message_interface import message_interface

class item:

    def __init__(self, data: dict):
        for k, v in data.items():
            if isinstance(v, list): setattr(self, k, read_list(v))
            elif isinstance(v, dict): setattr(self, k, item(v))
            else: setattr(self, k, v)

class Message_Event:

    handler: message_interface
    raw_data: dict
    event_type: str

    def __init__(self, message: dict, handler: message_interface):
        for k, v in message.items():
            if isinstance(v, list): setattr(self, k, read_list(v))
            elif isinstance(v, dict): setattr(self, k, item(v))
            else: setattr(self, k, v)
        self.raw_data = message
        self.handler = handler
        self.indetify_message_type()

    def group_or_private(self):
        if self.raw_data.get("group_id", None):
            return "group_"
        return "private_"

    def indetify_message_type(self):
        post_type = self.raw_data.get("post_type", "")
        if post_type == "message":
            event_type = f"{self.group_or_private()}message"
        elif post_type in ("notice", "request"):
            type_key = f"{post_type}_type"
            event_name = str(self.raw_data.get(type_key, ""))
            sub_type = str(self.raw_data.get("sub_type", ""))
            parts = (event_name, sub_type)
            prefix = "" if any(
                scope in value for value in parts for scope in ("group", "private")
            ) else self.group_or_private()
            event_type = prefix + event_name + (f"_{sub_type}" if sub_type else "")
        else:
            event_type = "undefined"
        self.event_type = event_type

    def reply_message(self, message):
        reply_message = MessageChain([])
        message_id = self.raw_data.get("message_id", None)
        user_id = self.raw_data.get("user_id", None)
        group_id = self.raw_data.get("group_id", None)
        if message_id is not None:
            reply_message.add(ReplyMessage(message_id))
        if user_id is not None and self.raw_data.get("message_type") == "group":
            reply_message.add(AtMessage(str(user_id)))
        if isinstance(message, Message_Event):
            message = message.to_send_message()
        if isinstance(message, NodeMessage):
            message = ForwardChain(message=message)
        if isinstance(message, ForwardChain):
            return self.handler.send_forward_msg(message=message, user_id=user_id, group_id=group_id)
        try:
            reply_message.add(message)
        except TypeError as e:
            reply_message = message
        return self.handler.send_msg(message=reply_message, user_id=user_id, group_id=group_id)

    def reply_poke(self):
        user_id = self.raw_data.get("user_id", None)
        group_id = self.raw_data.get("group_id", None)
        return self.handler.send_poke(user_id=user_id, group_id=group_id)

    def reply_face(self, id: int):
        message_id = self.raw_data.get("message_id", None)
        return self.handler.set_msg_emoji_like(message_id=message_id, emoji_id=id)

    def to_send_message(self) -> Message:
        if self.raw_data.get("post_type") == "message":
            messages = []
            for message in self.raw_data.get("message", []):
                message = self.handler.adapter.message_class(message)
                if message:
                    messages.append(message)
            if len(messages) > 1:
                message = MessageChain(message=messages)
            elif len(messages) == 1:
                message = messages[0]
            else:
                return None
            return message
        return None

def read_list(items: list):
    temp = []
    for i in items:
        if isinstance(i, list): temp.append(read_list(items=i))
        elif isinstance(i, dict): temp.append(item(data=i))
        else: temp.append(i)
    return temp