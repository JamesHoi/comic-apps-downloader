# comic-apps-downloader
 利用mitmproxy抓取日本漫画app漫画图片

# 支持的app
- [x] GGO
- [x] 漫画one
- [x] 漫画up
- [x] 漫画mee
- [x] パルシィ
- [x] サイコミ
- [x] コミックdays
- [x] マガポケ
- [ ] 漫画park
- [ ] COMIC FUZ
- [ ] lineマンガ

# 使用教程
打开软件：  
[![s1qV7n.png](https://s3.ax1x.com/2021/01/11/s1qV7n.png)](https://imgchr.com/i/s1qV7n)  
前置代理端口：电脑的代理服务器，以ssr为例（如下图），默认是1080  
抓包端口：手机需要连的代理端口  
线程数：自选  
[![s1qQcF.png](https://s3.ax1x.com/2021/01/11/s1qQcF.png)](https://imgchr.com/i/s1qQcF)

然后让手机和电脑同一网络下并设置抓包代理，服务器ip为电脑，端口为软件设置时所填  
<img src="https://s3.ax1x.com/2021/01/11/s1qnhV.png" alt="s1qnhV.png" border="0" style="zoom:25%"/>  

当前测试手机为`Android 10`下安装`HttpCanary`、`平行空间`且安装信任证书  
（貌似还需要安装`mitmproxy`证书，自行百度）  
真机则在平行空间下开启，模拟器需要安装xposed框架后再安装`JustTrustMe`  

然后点开任意一话漫画，程序会接受到数据并开始下载，并打包为zip  
[![s1qKpT.png](https://s3.ax1x.com/2021/01/11/s1qKpT.png)](https://imgchr.com/i/s1qKpT)
[![s1qM1U.png](https://s3.ax1x.com/2021/01/11/s1qM1U.png)](https://imgchr.com/i/s1qM1U)


