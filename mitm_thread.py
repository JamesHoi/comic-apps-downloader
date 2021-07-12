from threading import Thread
from mitmproxy.tools.main import mitmdump
import sys,os,asyncio


def program_dir():
    return sys._MEIPASS + "\\" if hasattr(sys, 'frozen') else os.getcwd() + "\\"


class Mitm_Listener(Thread):
    def __init__(self,port,front_port,socket_port,debug=False):
        super().__init__()
        self.port = port
        self.front_port = front_port
        self.socket_port = socket_port
        self.debug = debug

    def replace_file(self, filename, src, dest):
        with open(filename, "r", encoding="UTF-8") as f1: content = f1.read()
        with open(filename, "w", encoding="UTF-8") as f2: f2.write(content.replace(src, dest))

    def run(self):
        self.replace_file(program_dir() + "listener.py", "555555", self.socket_port)
        print("已启动抓包监听程序")
        asyncio.set_event_loop(asyncio.new_event_loop())
        mitmdump(["-p", self.port, "--mode", "upstream:http://127.0.0.1:" + self.front_port, "-s",
                  program_dir() + "listener.py","-q"])
        # -q console will not show