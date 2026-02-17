#引用库
import time, os
import builtins as __builtin__

#系统时间 => 日志文件名字
current_time = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
loger_time = time.strftime("%Y-%m-%d", time.localtime()) #每日轮换文件


#日志写入
def print(data: str = ""):
    #每日轮换文件
    today = time.strftime("%Y-%m-%d", time.localtime()) 
    global current_time
    global loger_time
    if today != loger_time: 
        loger_time = time.strftime("%Y-%m-%d", time.localtime()) 
    #后台打印
    __builtin__.print(data)
    #文件写入
    if not os.path.isdir("log"): os.makedirs("log")
    file = open(f'log/OneBotConnecter_{current_time}.log', 'a', encoding="utf-8")
    file.write(f"{data}\n")
    file.close()