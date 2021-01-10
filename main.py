from multiprocessing import freeze_support
from mitm_thread import Mitm_Listener
from download_thread import Download_Thread

import os
os.environ["mitm_debug"] = str(False)

if __name__ == '__main__':
    freeze_support()
    # 获取输入
    front_port = input("前置代理端口？") #str(1080)  #
    port = input("抓包端口？") # str(8050)  #
    socket_port = str(1234)  # input("通信端口？")
    thread_num = int(input("线程数？"))

    # 启动抓包监听
    listener = Mitm_Listener(port, front_port, socket_port)
    listener.start()

    # 启动抓包分析并下载
    download_thread = Download_Thread(socket_port, thread_num)
    download_thread.join()

