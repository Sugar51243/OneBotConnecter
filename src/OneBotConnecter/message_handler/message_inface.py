
from __future__ import annotations

from typing import TYPE_CHECKING

from OneBotConnecter.connecter.connecter import connecter
from OneBotConnecter.types.message import Message
from OneBotConnecter.types.chain.message_chain import MessageChain
from OneBotConnecter.types.chain.forward_chain import ForwardChain

if TYPE_CHECKING:
    from OneBotConnecter.adapters.message_interpreter import message_interpreter


class message_inface:

    inface: connecter
    adapter: message_interpreter

    def __init__(self, inface, adapter):
        self.inface = inface
        self.adapter = adapter

    def send_msg(self, message, user_id=None, group_id=None):
        if group_id is not None:
            return self.send_group_msg(group_id, message)
        return self.send_private_msg(user_id, message)

    def _message_to_datapack(self, message: Message):
        if not isinstance(message, MessageChain):
            if message.can_add_to_chain:
                message = MessageChain(message=message)
                message = message.to_send_message()
            else:
                message = [message.to_send_message()]
        else: message = message.to_send_message()
        return message

    def send_private_msg(self, user_id: int, message: Message):
        message = self._message_to_datapack(message)
        data = {
            "user_id": user_id,
            "message": message
        }
        return self.inface.send_to_server(action="send_private_msg", body=data)

    def send_group_msg(self, group_id: int, message: Message):
        message = self._message_to_datapack(message)
        data = {
            "group_id": group_id,
            "message": message
        }
        return self.inface.send_to_server(action="send_group_msg", body=data)

    def send_forward_msg(self, message, user_id=None, group_id=None):
        if group_id is not None:
            return self.send_group_forward_msg(group_id, message)
        return self.send_private_forward_msg(user_id, message)

    def send_private_forward_msg(self, user_id: int, message: Message):
        if not isinstance(message, ForwardChain):
            message = ForwardChain(message)
        data = message.to_send_message()
        data.update({"user_id": user_id})
        return self.inface.send_to_server(action="send_private_forward_msg", body=data)

    def send_group_forward_msg(self, group_id: int, message: Message):
        if not isinstance(message, ForwardChain):
            message = ForwardChain(message)
        data = message.to_send_message()
        data.update({"group_id": group_id})
        return self.inface.send_to_server(action="send_group_forward_msg", body=data)

    def send_poke(self, user_id: int, group_id:int = None, target_id: int = None):
        data = {
            "group_id": group_id,
            "user_id": user_id,
            "target_id": target_id
        }
        return self.inface.send_to_server(action="send_poke", body=data)

    def set_msg_emoji_like(self, message_id: int, emoji_id: int = 0, set: bool = True):
        data = {
            "message_id": message_id,
            "emoji_id": emoji_id,
            "set": set
        }
        return self.inface.send_to_server(action="set_msg_emoji_like", body=data)

    