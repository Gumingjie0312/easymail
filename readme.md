# 🚀one command to send email!

<div align=center>
<img src="icon.jpg"/>
</div>

# introduce
## this is a python powered script,by using it you can use only one command to send email,images and files to extra targets
 
# getting start
## you should have python > 3.6!!!

if you first run it, you may config something

```
C:\users\Joe>python easymail.py
未检测到配置文件
stmp服务器:your mailhost
授权码:your license code
您的邮箱:your email
已成功创建配置文件
```

then run
```
C:\users\Joe>python easymail --help
usage: easymail.py [-h] [-u USER [USER ...]] [-t TITLE] [-c CONTENT] [-l LOG] [--text TEXT] [--image IMAGE [IMAGE ...]]
                   [--file FILE [FILE ...]]

optional arguments:
  -h, --help            show this help message and exit
  -u USER [USER ...], --user USER [USER ...]
                        你想发送的对象,支持多个,使用空格连接
  -t TITLE, --title TITLE
                        你想发送的标题
  -c CONTENT, --content CONTENT
                        你想发送的内容
  -l LOG, --log LOG     是否记录日志 true:记录 false:不记录
  --text TEXT           你想发送的内容(本地文件的路径)
  --image IMAGE [IMAGE ...]
                        你想发送的图片的路径,支持多个,使用空格连接
  --file FILE [FILE ...]
                        你想发送的附件的路径,支持多个,使用空格连接
```
