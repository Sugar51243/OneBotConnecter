
from __future__ import annotations

from typing import TYPE_CHECKING

from OneBotConnecter.connecter.connecter import connecter
from OneBotConnecter.types.message import Message
from OneBotConnecter.types.chain.message_chain import MessageChain
from OneBotConnecter.types.chain.forward_chain import ForwardChain

if TYPE_CHECKING:
    from OneBotConnecter.adapters.message_interpreter import message_interpreter


class message_interface:

    inface: connecter
    adapter: message_interpreter

    def __init__(self, inface, adapter, bot):
        self.inface = inface
        self.adapter = adapter
        self.bot = bot

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

    def delete_msg(self, message_id: int):
        data = {"message_id": message_id}
        return self.inface.send_to_server(action="delete_msg", body=data)

    def get_msg(self, message_id: int):
        data = {"message_id": message_id}
        return self.inface.send_to_server(action="get_msg", body=data)

    def get_forward_msg(self, forward_id: str):
        data = {"id": forward_id}
        return self.inface.send_to_server(action="get_forward_msg", body=data)

    def send_like(self, user_id: int, times: int = 1):
        data = {
            "user_id": user_id,
            "times": times
        }
        return self.inface.send_to_server(action="send_like", body=data)

    def set_group_kick(self, group_id: int, user_id: int, reject_add_request: bool = False):
        data = {
            "group_id": group_id,
            "user_id": user_id,
            "reject_add_request": reject_add_request
        }
        return self.inface.send_to_server(action="set_group_kick", body=data)

    def set_group_ban(self, group_id: int, user_id: int, duration: int = 30 * 60):
        data = {
            "group_id": group_id,
            "user_id": user_id,
            "duration": duration
        }
        return self.inface.send_to_server(action="set_group_ban", body=data)

    def set_group_anonymous_ban(self, group_id: int, anonymous=None, anonymous_flag: str = None,
                                duration: int = 30 * 60):
        data = {
            "group_id": group_id,
            "anonymous": anonymous,
            "anonymous_flag": anonymous_flag,
            "duration": duration
        }
        return self.inface.send_to_server(action="set_group_anonymous_ban", body=data)

    def set_group_whole_ban(self, group_id: int, enable: bool = True):
        data = {
            "group_id": group_id,
            "enable": enable
        }
        return self.inface.send_to_server(action="set_group_whole_ban", body=data)

    def set_group_admin(self, group_id: int, user_id: int, enable: bool = True):
        data = {
            "group_id": group_id,
            "user_id": user_id,
            "enable": enable
        }
        return self.inface.send_to_server(action="set_group_admin", body=data)

    def set_group_anonymous(self, group_id: int, enable: bool = True):
        data = {
            "group_id": group_id,
            "enable": enable
        }
        return self.inface.send_to_server(action="set_group_anonymous", body=data)

    def set_group_card(self, group_id: int, user_id: int, card: str = ""):
        data = {
            "group_id": group_id,
            "user_id": user_id,
            "card": card
        }
        return self.inface.send_to_server(action="set_group_card", body=data)

    def set_group_name(self, group_id: int, group_name: str):
        data = {
            "group_id": group_id,
            "group_name": group_name
        }
        return self.inface.send_to_server(action="set_group_name", body=data)

    def set_group_leave(self, group_id: int, is_dismiss: bool = False):
        data = {
            "group_id": group_id,
            "is_dismiss": is_dismiss
        }
        return self.inface.send_to_server(action="set_group_leave", body=data)

    def set_group_special_title(self, group_id: int, user_id: int, special_title: str = "",
                                duration: int = -1):
        data = {
            "group_id": group_id,
            "user_id": user_id,
            "special_title": special_title,
            "duration": duration
        }
        return self.inface.send_to_server(action="set_group_special_title", body=data)

    def set_friend_add_request(self, flag: str, approve: bool = True, remark: str = ""):
        data = {
            "flag": flag,
            "approve": approve,
            "remark": remark
        }
        return self.inface.send_to_server(action="set_friend_add_request", body=data)

    def set_group_add_request(self, flag: str, sub_type: str, approve: bool = True, reason: str = ""):
        data = {
            "flag": flag,
            "sub_type": sub_type,
            "approve": approve,
            "reason": reason
        }
        return self.inface.send_to_server(action="set_group_add_request", body=data)

    def get_login_info(self):
        return self.inface.send_to_server(action="get_login_info", body={})

    def get_stranger_info(self, user_id: int, no_cache: bool = False):
        data = {
            "user_id": user_id,
            "no_cache": no_cache
        }
        return self.inface.send_to_server(action="get_stranger_info", body=data)

    def get_friend_list(self):
        return self.inface.send_to_server(action="get_friend_list", body={})

    def get_group_info(self, group_id: int, no_cache: bool = False):
        data = {
            "group_id": group_id,
            "no_cache": no_cache
        }
        return self.inface.send_to_server(action="get_group_info", body=data)

    def get_group_list(self):
        return self.inface.send_to_server(action="get_group_list", body={})

    def get_group_member_info(self, group_id: int, user_id: int, no_cache: bool = False):
        data = {
            "group_id": group_id,
            "user_id": user_id,
            "no_cache": no_cache
        }
        return self.inface.send_to_server(action="get_group_member_info", body=data)

    def get_group_member_list(self, group_id: int):
        data = {"group_id": group_id}
        return self.inface.send_to_server(action="get_group_member_list", body=data)

    def get_group_honor_info(self, group_id: int, honor_type: str):
        data = {
            "group_id": group_id,
            "type": honor_type
        }
        return self.inface.send_to_server(action="get_group_honor_info", body=data)

    def get_cookies(self, domain: str = ""):
        data = {"domain": domain}
        return self.inface.send_to_server(action="get_cookies", body=data)

    def get_csrf_token(self):
        return self.inface.send_to_server(action="get_csrf_token", body={})

    def get_credentials(self, domain: str = ""):
        data = {"domain": domain}
        return self.inface.send_to_server(action="get_credentials", body=data)

    def get_record(self, file: str, out_format: str):
        data = {
            "file": file,
            "out_format": out_format
        }
        return self.inface.send_to_server(action="get_record", body=data)

    def get_image(self, file: str):
        data = {"file": file}
        return self.inface.send_to_server(action="get_image", body=data)

    def can_send_image(self):
        return self.inface.send_to_server(action="can_send_image", body={})

    def can_send_record(self):
        return self.inface.send_to_server(action="can_send_record", body={})

    def get_status(self):
        return self.inface.send_to_server(action="get_status", body={})

    def get_version_info(self):
        return self.inface.send_to_server(action="get_version_info", body={})

    def set_restart(self, delay: int = 0):
        data = {"delay": delay}
        return self.inface.send_to_server(action="set_restart", body=data)

    def clean_cache(self):
        return self.inface.send_to_server(action="clean_cache", body={})

    