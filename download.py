import os,shutil,requests,time
from PIL import Image
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from concurrent.futures import as_completed,ThreadPoolExecutor,ProcessPoolExecutor


def downloadFile(url, path, name):
    while True:
        try:
            r = requests.get(url, stream=True, verify=False,timeout=5)
            if r.status_code == 404: return False
            break
        except requests.exceptions.ConnectionError: time.sleep(2)
        except requests.exceptions.ReadTimeout: time.sleep(2)
    with open(path + name, 'wb') as f: f.write(r.content)
    return True


def webp2jpg(path,input_name, output_name):
    im = Image.open(path+input_name)
    if im.mode == "RGBA":
        im.load()  # required for png.split()
        background = Image.new("RGB", im.size, (255, 255, 255))
        background.paste(im, mask=im.split()[3])  # 3 is the alpha channel
        im = background
    im.save('{}.jpg'.format(path+output_name), 'JPEG',quality=95,subsampling=0)


def downloadPath(path_name="img"):
    i = 0
    while True:
        path = path_name+"_{}".format(i)
        if not os.path.exists(path) and not os.path.exists(path+".zip"):
            os.mkdir(path);break
        else: i += 1
    return path


def downloadComic(url,folder_name,page,img_type="webp",zero_fill=3):
    page_name = str(page+1).zfill(zero_fill)
    file_name = page_name +"."+img_type
    downloadFile(url, folder_name + "/", file_name)
    if img_type == "webp":
        webp2jpg(folder_name + "/", file_name, page_name)
        os.remove(folder_name + "/" + file_name)
    print("已完成下载第{}页".format(page+1))


def downloadAll(urls,thread_num,img_type="webp",path_name="img",is_pack=True):
    folder_name = downloadPath(path_name=path_name)
    if not os.path.exists(folder_name): os.mkdir(folder_name)
    executor = ProcessPoolExecutor(max_workers=thread_num)  # ThreadPoolExecutor(max_workers=thread_num)
    all_task = [executor.submit(downloadComic,urls[i],folder_name,i
                ,img_type=img_type,zero_fill=3 if len(urls)<=100 else 4) for i in range(len(urls))]
    for i in range(len(urls)): print(str(i).zfill(3)+".webp: "+ urls[i])  # 方便手动补全
    print("初始化完成，开始下载")
    for future in as_completed(all_task): pass # 等待线程完成
    if is_pack:
        shutil.make_archive(folder_name, 'zip', folder_name)
        shutil.rmtree(folder_name)
    print("已下载完成")
