import argparse
import json
import os
import smtplib
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def main():
    mm = MIMEMultipart('related')
    if not os.path.exists("config.json"):
        createconfig()
    with open('config.json', encoding='utf-8') as file_obj:
        contents = file_obj.read()
        try:
            jsons = json.loads(contents.rstrip())
        except json.decoder.JSONDecodeError:
            print("err json配置错误")
            os._exit(0)
        try:
            mail_host = jsons["mail_host"]
            mail_license = jsons["mail_license"]
            mail_sender = jsons["mail_sender"]
            mm["From"] = mail_sender
        except KeyError:
            print("err json配置错误")
            os._exit(0)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u", "--user", help="你想发送的对象,支持多个,使用空格连接", type=str, nargs='+')
    parser.add_argument("-t", "--title", help="你想发送的标题", type=str)
    parser.add_argument("-c", "--content", help="你想发送的内容", type=str)
    parser.add_argument(
        "-l", "--log", help="是否记录日志 true:记录  false:不记录", type=bool)
    parser.add_argument("--text", help="你想发送的内容(本地文件的路径)", type=str)
    parser.add_argument(
        "--image", help="你想发送的图片的路径,支持多个,使用空格连接", type=str, nargs='+')
    parser.add_argument(
        "--file", help="你想发送的附件的路径,支持多个,使用空格连接", type=str, nargs='+')
    args = parser.parse_args()
    if args.title:
        mm["Subject"] = Header(args.title, 'utf-8')
    else:
        print("err 没有标题\n查看帮助 -h 或 -help")
        os._exit(0)
    if args.user:
        if (len(args.user)) == 1:
            mm["To"] = "receiver_1_name<"+args.user[0]+">"
        else:
            recieves = []
            for i in range(len(args.user)):
                recieves.append("receiver_"+str(i+1)+"_name<"+args.user[i]+">")
            mm["To"] = ",".join(recieves)
    else:
        print("err 没有目标")
        os._exit(0)
    if args.content and args.text:
        print("err 命令冲突")
        os._exit(0)
    elif args.content:
        message_text = MIMEText(args.content, "plain", "utf-8")
        mm.attach(message_text)
    elif args.text:
        try:
            with open(args.text, encoding='utf-8') as files:
                contents = files.read()
                print("检测发送内容为文件:")
                print(contents.rstrip())
                message_text = MIMEText(contents.rstrip(), "plain", "utf-8")
                mm.attach(message_text)
        except FileNotFoundError:
                print("err 文件不存在!!!")
                os._exit(0)
    else:
        print("err 没有内容")
        os._exit(0)
    if args.image:
        for i in range(len(args.image)):
            item = args.image[i]
            try:
                image_data = open(item, 'rb')
            except FileNotFoundError:
                print("err 图片不存在!!!")
                os._exit(0)
            message_image = MIMEImage(image_data.read())
            image_data.close()
            ext = item.split(".")
            message_image.add_header(
                'Content-Disposition', 'attachment', filename="图片"+str(i+1)+"."+ext[len(ext)-1])
            mm.attach(message_image)
    if args.file:
        for i in range(len(args.file)):
            item = args.file[i]
            ext = item.split("\\")
            try:
                att = MIMEText(open(item, 'rb').read(), 'base64', 'utf-8')
            except FileNotFoundError:
                print("err 附件不存在!!!")
                os._exit(0)
            att["Content-Disposition"] = "attachment; filename='" + \
                ext[len(ext)-1]+"'"
            mm.attach(att)
    if args.log:
        islog = 1
    else:
        islog = 0
    try:
        stp = smtplib.SMTP()
        stp.set_debuglevel(islog)
        stp.connect(mail_host, 25)
        stp.login(mail_sender, mail_license)
        stp.sendmail(mail_sender, args.user, mm.as_string())
        stp.quit()
        print("发送成功")
    except smtplib.SMTPDataError as e:
        print("err 发送失败")
        print(e)
    except smtplib.SMTPAuthenticationError:
        print("err 登录失败")


def createconfig():
    print("未检测到配置文件")
    mail_host = input("stmp服务器:")
    mail_license = input("授权码:")
    mail_sender = input("您的邮箱:")
    data = {
        "mail_host": mail_host,
        "mail_license": mail_license,
        "mail_sender": mail_sender
    }
    data = json.dumps(data)
    with open("config.json","w") as a:
        a.write(data)
    print("已成功创建配置文件")


if __name__ == "__main__":
    main()