# OneBotConnecter
本项目为onebot协议的非官方python整合, 允许用户快捷连接ws服务器，并收发信息。<br>
本项目基于ll2接口开发。理论上面对其他基于onebot-11协议的接口同样可以运行，但是毕竟没实际测试过，本人不担保可以100%顺利运行。

### !!!!!!
项目本身不包括任何机器人接口，请自行安装支持onebot协议的机器人接口并完成登录，再运行本项目!!!

## 项目结构
项目本身仅包括两个文件，OneBot.py及MessageType.py。<br>
OneBot负责服务器的直接连接及信息的IO处理。<br>
MessageType负责信息发送的数据包构造。<br>
换而言之，需要 查询/修改 对服务器直接交互或信息收集行为的情况下，请直接查询或修改 [OneBot.py](https://github.com/Sugar51243/OneBotConnecter/blob/main/src/OneBotConnecter/OneBot.py)。需要 查询/修改 向服务器发送的数据包内容或格式，请直接查询或修改 [MessageType.py](https://github.com/Sugar51243/OneBotConnecter/blob/main/src/OneBotConnecter/MessageType.py)。

## 使用教程
本项目基于python异步运行，请确保asyncio库已被引入。<br>
使用方法很简单:<br>
1.构造收集到信息时需要运行的脚本函数，填入参数为(机器人本体bot, 信息数据包message)<br>
2.通过本库创建OneBot对象并填入机器人基本信息，填入参数为(服务器地址, 管理员id, 机器人别称)<br>
3.运行对象的run函数，并填入1步骤的脚本函数为参数，开始连接并监听服务器推送<br>
具体可参考本项目的[example文件](https://github.com/Sugar51243/OneBotConnecter/blob/main/test/main.py)，个人认为已经写得很清楚了。

## 安装
`pip install OneBotConnecter==0.1.1`
