import socket,json

s = socket.socket()  # 创建 socket 对象
port = 1234  # 设置端口号
s.connect(("127.0.0.1", port))

filter_url = [
    {
        "name": "GGO",
        "url": ["https://api-ggo.tokyo-cdn.com/api/viewer/manga_data"],
        "url_not": [], "find_encoding": "byte",
        "find": ["https://api-ggo.tokyo-cdn.com/secure"],
        "find_not":["title_thumbnail_list_single","extra_manga_page"],
        "ending": ["expires"],
        "find_mode":"normal","type": "comic","img_type": "webp"
    },
    {
        "name": "漫画one",
        "url":["https://app.manga-one.com/api/v3/viewer?chapter_id="],
        "url_not": [], "find_encoding": "str",
        "find":["https://app.manga-one.com/secure","webp"],
        "find_not":[], "ending":[],
        "find_mode":"normal","type":"comic","img_type": "webp"
    },
    {
        "name": "漫画up",
        "url":["https://ja-android.manga-up.com/v1/api/read.php"],
        "url_not": [],"find_encoding": "str",
        # head是选择最顶为父节点，child是page的子节点，parent是pages父节点，node是pages自身节点
        "pages_parent": "data", "page_child": "url","pages_node":"pages",
        "find_mode":"json", "type":"comic","img_type": "webp"
    },
    {
        "name": "漫画mee",
        "url":["https://prod-android.manga-mee.jp/api/v1/viewer"],
        "url_not": [],"find_encoding": "str",
        "find":["https://prod-img.manga-mee.jp/secure","webp","manga_page"],
        "find_not":[], "ending":[],
        "find_mode":"normal", "type":"comic","img_type": "webp"
    },
    {
        "name": "パルシィ",
        "url":["https://api.palcy.jp/api/v3/episodes/","buy"],
        "url_not":["confirm"],"find_encoding": "str",
        "find_not":[], "ending": [],
        # head是选择最顶为父节点，child是page的子节点，parent是pages父节点，node是pages自身节点
        "pages_parent": "head", "page_child": "imageUrl", "pages_node": "pages",
        "find_mode": "json" ,"type": "comic","img_type": "webp"
    },
    {
        "name":"サイコミ",
        "url": ["https://api.cycomi.com/fw/cycomiapi/chapter/pages"],
        "url_not": [],"find_encoding": "str",
        "find_not": [], "ending": [],
        # head是选择最顶为父节点，child是page的子节点，parent是pages父节点，node是pages自身节点
        "pages_parent": "head", "page_child": "image", "pages_node": "pages",
        "find_mode": "json", "type": "comic","img_type": "webp"
    },
    {
        "name": "コミックdays",
        "url": ["https://comic-days.com/api/v1/episode/","viewer"],
        "url_not": [],"find_encoding": "str",
        "find_not": [], "ending": [],
        # head是选择最顶为父节点，child是page的子节点，parent是pages父节点，node是pages自身节点
        "pages_parent": "head", "page_child": "array", "pages_node": "image_uris",
        "find_mode": "json", "type": "comic","img_type": "jpg"
    },
    {
        "name":"マガポケ",
        "url": ["https://mgpk-api.magazinepocket.com/episode/viewer"],
        "url_not": [],"find_encoding": "str",
        "find_not": [],"ending": [],
        # head是选择最顶为父节点，child是page的子节点，parent是pages父节点，node是pages自身节点
        "pages_parent": "head", "page_child": "image_url", "pages_node": "page_list",
        "find_mode": "json", "type": "comic","img_type": "jpg"
    }
]


def send_content(content):
    s.send("content-lengths:{}".format(len(content)).encode())
    s.recv(1024)  # 阻塞，等待另一个线程处理数据完毕后再发送
    s.send(content)


def response(flow):
    for data in filter_url:
        contains = [key in flow.request.url for key in data["url"]]
        for key in data["url_not"]: contains.append(key not in flow.request.url)
        if False not in contains: break
    else: return
    if data["find_encoding"] == "byte": data["content"] = str(flow.response.content)
    data["content"] = flow.response.content.decode("utf-8","ignore")
    send_content(bytes(json.dumps(data).encode()))
