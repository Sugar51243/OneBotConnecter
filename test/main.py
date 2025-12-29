#=====须知=====#

#--本项目为OneBotConnecter，为onebot协议的非官方python整合连接器
#--本项目允许用户通过python快捷连接ws服务器，收发信息，并开发机器人脚本。

#--此项目基于ll2接口开发。虽然理论上面对其他基于onebot协议的接口同样可以运行，但是毕竟没实际测试过，本人不担保可以100%顺利运行。
#--项目本身不包括任何机器人接口，请自行安装支持onebot协议的机器人接口并完成登录，再运行本项目


#==此脚本为OneBotConnecter的基础演示例，具体使用方法请参考readme文件==#

#导入必要的库
import asyncio
from OneBotConnecter.OneBot import OneBot
from OneBotConnecter.MessageType import MessageChain

#收到信息时运行的脚本
async def onMessage(bot, message):
    if bot.testMode == True:
        #打印数据包
        print(message)
    #如果收到的信息为: 测试
    if message["raw_message"] == "测试":
        #回复: 脚本连接成功
        msg = MessageChain(["脚本连接成功"])
        #信息发送后服务器会有回应，函数已尝试收集回应，可以自行打印
        #或者在调试模式下自动收集并打印
        callback = await bot.send_private_msg(user_id = message["sender"]["user_id"], message = msg)

#主函数
if __name__ == "__main__":
    #创建OneBot对象
    bot = OneBot(uri="ws://127.0.0.1:3001", owner=[], botName=[])
    #开启调试模式
    #注意调试模式会尝试于后台打印所有向服务器的收发信息，平时建議关闭
    await bot.test(True)
    #通过WS连接对象，并开始监听信息推送
    asyncio.run(bot.run(on_message=onMessage))
