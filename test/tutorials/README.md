# Tutorials

这些案例都需要一个已经登录的 OneBot 11 正向 WebSocket 服务端。默认地址是 `ws://127.0.0.1:3001`，也可以修改各文件顶部的 `WS_URL`。

请在项目根目录运行：

```bash
python test/tutorials/01_echo.py
```

| 文件 | 用途 | 触发方式 |
| --- | --- | --- |
| `01_echo.py` | 基础回呼、异常处理、文字回复 | 发送 `test` |
| `02_message_chain.py` | 组合文字、At、图片 | 发送 `chain` |
| `03_inspect_event.py` | 查看事件字段和讯息段 | 发送 `inspect` |
| `04_api_calls.py` | 查询登录信息、主动发消息 | 发送 `info` 或 `send` |
| `05_forward_message.py` | 建立合并转发消息 | 发送 `forward` |
| `06_account_info.py` | 从回呼的 `bot` 参数读取账号属性 | 发送 `account` |

## 回呼约定

```python
def on_message(bot, message):
    # bot 是 message_interface；message 是 Message_Event
    pass
```

案例中的 `bot` 是 `message_interface`，可调用 OneBot API；实际的 `OneBot` 连接器实例位于 `bot.bot`。因此连接器账号属性要从 `bot.bot` 读取：`user_id`、`nickname` 和 `owner`。`message` 可使用 `raw_data`、`raw_message`、`event_type` 和 `reply_message` 等成员。涉及真实 API 的案例必须连接服务端才能看到效果；仅导入和消息序列化则不需要网络。