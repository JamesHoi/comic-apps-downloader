from threading import Thread
import socket, math, re, json
from download import downloadAll


class Download_Thread(Thread):
    def __init__(self, socket_port,thread_num):
        super(Download_Thread, self).__init__()
        self.s = socket.socket()
        self.s.bind(("127.0.0.1", int(socket_port)))
        self.s.listen(5)
        self.buffer_size = 4096
        self.thread_num = thread_num
        self.start()

    def recv_content(self, c):
        data = str(c.recv(self.buffer_size))
        c.send(data.encode())  # 让对方知道已接收到长度大小
        content_len = int(data[data.find(":") + 1:-1])
        buffer = bytes(); times = math.ceil(content_len / self.buffer_size)
        for i in range(times):
            buffer += c.recv(self.buffer_size if not i + 1 == times else content_len)
        return buffer

    def find_url_normally(self, data):
        urls = re.findall("(?P<url>https?://[^\s]+)", data["content"])  # 找出所有http链接
        def filter_fun(url):
            contains = [key in url for key in data["find"]]
            for key in data["find_not"]: contains.append(key not in url)
            contains.append(url.startswith(data["find"][0]))
            return False not in contains
        urls = list(filter(filter_fun, urls))  # 过滤掉不需要的链接
        for text in data["ending"]:
            if text == "expires":  urls = [url[:url.find("expires")+18] for url in urls]
            else: urls = [url[:url.find(text)] for url in urls]  # 以某个字串做结尾，删除结尾后面的文字
        return urls

    def find_url_by_json(self,data):
        comic_data = json.loads(data["content"])
        if data["pages_parent"] == "head": parent = comic_data
        else: parent = comic_data[data["pages_parent"]]
        child = data["page_child"]; pages = parent[data['pages_node']]; urls = []
        if child == "array": return pages
        for page in pages:
            if child in page: urls.append(page[child])
        return urls

    def find_url(self,data):
        if data["find_mode"] == "normal": return self.find_url_normally(data)
        elif data["find_mode"] == "json": return self.find_url_by_json(data)
        else: return []

    def indexstr(self,src, key):
        indexstr2 = []; i = 0
        while key in src[i:]:
            indextmp = src.index(key, i, len(src))
            indexstr2.append(indextmp)
            i = (indextmp + len(key))
        return indexstr2

    def find_close(self,arr, src):
        new_arr = [src-num for num in arr if src-num > 0]
        return new_arr.index(min(new_arr))

    def find_japanese_str(self,src,start):
        head = 0; end = 0
        def isJapanese(char):
            return (char >= '\u30a0' and char <= '\u30ff') or \
                   (char>='\u4e00' and char <='\u9fa5') or \
                   (char>='\u3040' and char <='\u309f') or \
                   char == " "
        while True:
            if isJapanese(src[start + head]): break
            head += 1
        while True:
            if not isJapanese(src[start + head + end]): break
            end += 1
        return src[start+head:start+head+end]

    def find_name_normally(self,data):
        app_name = data["name"]
        content = data["content"]
        if app_name == "GGO":
            all_key = self.indexstr(content, "#")
            end = content.find("https://app.ganganonline.com/sns_share")
            end_index = self.find_close(all_key,end)
            return content[all_key[end_index-1]+1:all_key[end_index]]
        elif app_name == "漫画one":
            all_key = self.indexstr(content, "#")
            return content[all_key[-2]+1:all_key[-1]]
        elif app_name == "漫画mee":
            start = content.find("次の話を読む")+6
            return self.find_japanese_str(content,start)
        else: return ""


    def find_name_by_json(self,data):
        comic_data = json.loads(data["content"])
        app_name = data["name"]
        if app_name == "漫画up": return comic_data["data"]["viewer"]["title_name"]
        elif app_name == "パルシィ": return comic_data["comic"]["title"]
        elif app_name == "サイコミ": return comic_data["title_name"]
        elif app_name == "コミックdays": return comic_data["current_episode"]["title"]
        elif app_name == "マガポケ": return comic_data["title_name"]

    def find_name(self,data):
        if data["find_mode"] == "normal": return self.find_name_normally(data)
        elif data["find_mode"] == "json": return self.find_name_by_json(data)
        else: return ""

    def validateTitle(self,title):
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        new_title = re.sub(rstr, "_", title)  # 替换为下划线
        return new_title

    def run(self):
        c, addr = self.s.accept()  # 建立客户端连接
        print("已成功与监听建立通信")
        while True:
            data = json.loads(self.recv_content(c).decode())
            if len(data["content"]) < 15: continue
            urls = self.find_url(data)
            comic_name = self.find_name(data)
            print("成功获取到软件\"{}\"的漫画\"{}\"，共{}页".format(data["name"],comic_name,len(urls)))
            if len(urls): downloadAll(urls,self.thread_num,
                    img_type=data["img_type"],path_name=self.validateTitle(comic_name))