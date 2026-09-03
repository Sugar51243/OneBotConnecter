
import json


class Message:
    """所有可轉換為 OneBot 發送訊息段的物件基類。"""

    # 特殊動作或內嵌物件可覆寫為 False，避免被加入 MessageChain。
    can_add_to_chain = True

    def to_send_message(self):
        data = {
            key: value for key, value in self.__dict__.items()
            if value is not None
        }
        data = json.loads(json.dumps(data, ensure_ascii=False, default=lambda item: item.to_send_message()))
        if getattr(self, "message_type", None):
            return {"type": self.message_type, "data": data}
        return data

    def merge(self, other):
        """合併相同訊息段的欄位，拒絕不同訊息段互相污染。"""
        if not isinstance(other, (Message, dict)):
            raise TypeError("只能合併 Message 或 dict")

        current_type = getattr(self, "message_type", None)
        other_type = getattr(other, "message_type", None)
        if isinstance(other, dict):
            other_type = other.get("type", other.get("message_type"))
        if current_type and other_type and current_type != other_type:
            raise TypeError(
                f"不可合併不同訊息段: {current_type} 與 {other_type}"
            )

        values = other.__dict__ if isinstance(other, Message) else dict(other)
        for key, value in values.items():
            if key not in ("message_type", "type") and value is not None:
                setattr(self, key, value)
        return self
