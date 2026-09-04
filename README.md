# OneBotConnecter

OneBotConnecter 是一个基于 OneBot 11 的 Python WebSocket 正向连接器，用于接收事件、发送消息和调用 OneBot API。项目不包含机器人实现或登录逻辑，使用前请先准备已登录并开放正向 WebSocket 的 OneBot 服务端。

## 安装

从 PyPI 安装：

```bash
python -m pip install OneBotConnecter
```

从源码安装（开发模式）：

```bash
git clone https://github.com/Sugar51243/OneBotConnecter.git
cd OneBotConnecter
python -m pip install -e .
```

项目要求 Python 3.9 或更高版本。安装依赖后，确认机器人服务端的 WebSocket 地址，例如 `ws://127.0.0.1:3001`。

## 快速开始

```python
from OneBotConnecter.Event.Message_Event import Message_Event
from OneBotConnecter.OneBot import OneBot


def on_message(bot, message: Message_Event):
    if message.raw_message == "test":
        message.reply_message("hello")


if __name__ == "__main__":
    bot = OneBot("ws://127.0.0.1:3001", on_message)
    bot.run()
```

`on_message` 的 `bot` 参数是 `message_interface`，`message` 参数是 `Message_Event`。连接器会自动根据事件中的 `user_id` 和 `group_id` 选择私聊或群聊回复。连接器本身可通过 `bot.bot` 取得，其账号属性为 `bot.bot.user_id`、`bot.bot.nickname` 和 `bot.bot.owner`。

更多可直接修改运行的案例位于 [`test/tutorials`](test/tutorials)：

- [`01_echo.py`](test/tutorials/01_echo.py)：文字指令与异常处理
- [`02_message_chain.py`](test/tutorials/02_message_chain.py)：文字、At、图片组成消息链
- [`03_inspect_event.py`](test/tutorials/03_inspect_event.py)：读取事件和解析收到的消息
- [`04_api_calls.py`](test/tutorials/04_api_calls.py)：调用查询接口与主动发送消息
- [`05_forward_message.py`](test/tutorials/05_forward_message.py)：发送合并转发消息
- [`README.md`](test/tutorials/README.md)：案例运行说明和接口速查

运行案例时，请在项目根目录执行，例如：

```bash
python test/tutorials/01_echo.py
```

## Message_Event

事件回呼中常用的属性和方法：

| 成员 | 说明 |
| --- | --- |
| `raw_message` | OneBot 原始文字内容 |
| `raw_data` | 完整的原始事件字典 |
| `event_type` | 事件类型，例如 `group_message`、`private_message` |
| `reply_message(message)` | 回复字符串、讯息段或 `MessageChain` |
| `reply_poke()` | 回复戳一戳 |
| `reply_face(id)` | 对当前消息发送表情回应 |
| `to_send_message()` | 将收到的消息转换为讯息对象 |

## 构造消息

讯息类型从 `OneBotConnecter.types` 导入：

```python
from OneBotConnecter.types import AtMessage, ImageMessage, MessageChain, TextMessage

message = MessageChain([
    TextMessage("你好 "),
    AtMessage(123456),
    ImageMessage("https://example.com/image.png"),
])
event.reply_message(message)
```

可用讯息段包括 `TextMessage`、`AtMessage`、`FaceMessage`、`ImageMessage`、`RecordMessage`、`ReplyMessage`、`VideoMessage`，以及 `DiceMessage`、`JsonMessage`、`MarkdownMessage`、`MusicMessage`、`RpsMessage`、`ShakeMessage`。`ForwardChain` 用于合并转发，详见案例。

`MessageChain` 也提供：

- `chain.text`：合并所有文字段
- `chain.texts`：取得文字段列表
- `chain.get("image")`：取得指定类型的讯息段
- `chain.to_send_message()`：转换为 OneBot message 数组

## bot API 速查

回呼中的 `bot` 可以直接调用以下接口：

| 类别 | 方法 |
| --- | --- |
| 发送 | `send_msg`、`send_private_msg`、`send_group_msg`、`send_forward_msg`、`send_like`、`send_poke` |
| 消息 | `get_msg`、`delete_msg`、`get_forward_msg`、`set_msg_emoji_like` |
| 群组 | `get_group_info`、`get_group_list`、`get_group_member_info`、`get_group_member_list`、`set_group_kick`、`set_group_ban`、`set_group_whole_ban`、`set_group_admin`、`set_group_card`、`set_group_name`、`set_group_leave`、`set_group_special_title` |
| 用户 | `get_login_info`、`get_stranger_info`、`get_friend_list` |
| 请求 | `set_friend_add_request`、`set_group_add_request` |
| 状态与资源 | `get_status`、`get_version_info`、`get_image`、`get_record`、`can_send_image`、`can_send_record` |

例如主动发送群消息：

```python
def on_message(bot, message):
    if message.raw_message == "send":
        bot.send_group_msg(123456, "主动发送的消息")
```

## 注意事项

- WebSocket 地址必须是 OneBot 服务端的正向 WebSocket 地址，并且服务端已登录。
- `set_group_kick`、`set_group_ban`、`set_restart` 等接口会改变账号或群组状态，请先确认权限和参数。
- 图片、语音和视频的 `file` 格式取决于 OneBot 实现，常见形式包括 URL、本地路径或服务端文件标识。
- 本项目主要按 OneBot 11 设计，其他实现可能存在扩展字段或行为差异。

## 项目结构

```text
OneBotConnecter/
├── src/OneBotConnecter/  # 连接器、事件、讯息类型
├── test/                 # 演示入口与 tutorials
├── pyproject.toml
├── README.md
└── LICENSE
```

## 许可证

本项目使用 MIT 许可证，详见 [LICENSE](LICENSE)。
