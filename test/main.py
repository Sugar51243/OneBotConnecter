#=====须知=====#

#--本项目为OneBotConnecter，为onebot协议的非官方python整合连接器
#--本项目允许用户通过python快捷连接ws服务器，收发信息，并开发机器人脚本。

#--此项目基于ll2接口开发。虽然理论上面对其他基于onebot协议的接口同样可以运行，但是毕竟没实际测试过，本人不担保可以100%顺利运行。
#--项目本身不包括任何机器人接口，请自行安装支持onebot协议的机器人接口并完成登录，再运行本项目


#==此脚本为OneBotConnecter的基础演示例，具体使用方法请参考readme文件==#
from OneBotConnecter.Event.Message_Event import Message_Event
from OneBotConnecter.message_handler import message_interface
from OneBotConnecter.OneBot import OneBot

#收到信息时运行的脚本
def onMessage(bot: message_interface, message: Message_Event):
    try:
        if message.raw_message == "test":
            message.reply_message("hello")
    except:
        print(message.raw_data)

#主函数
if __name__ == "__main__":
    #创建OneBot对象
    bot = OneBot("ws://127.0.0.1:3001", onMessage)
    #开始监听信息推送
    bot.run()
