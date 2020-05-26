import email_sender as es

# user_name = 'xiangwan@trinity.unimelb.edu.au'


# sender.send_eamil('Xianghao', receivers, '友善的问候', '有本事来我公寓打我啊！')

def login():
    sender = None

    while True:
        print('*******************************************')
        # 登陆信息输入
        print('请输入您的邮箱信息')
        user_name = input('请输入您的邮箱账户：')
        passsword = input('请输入您的密码：')

        print('登陆中.....')

        # 创建发送者
        sender = es.EmailSender.default(user_name, passsword)

        # 验证信息是否正确
        if sender.verificate():
            print('登陆成功！')
            break
        else:
            print('登陆失败，请检查网络或账号密码！')
            continue


    return sender

def read_content():
    with open('content.html', 'r') as f:
        return f.read()

def read_receivers():
    receivers = []
    with open('list.txt', 'r') as f:
        for line in f:
            receivers.append(line.strip())

    return receivers

def group_email(sender):
    print('*******************************************')
    print('请将邮件内容添加content.html, 收件人名单添加进list.txt')
    subject = input('请输入主题：')
    
    try:
        print('读取邮件内容.....')
        content = read_content()
    except Exception:
        print('未找到content.html，请将其放在根目录下！')
        return

    try:
        print('读取收件人.....')
        receivers = read_receivers()
    except Exception:
        print('未找到list.txt，请将其放在根目录下！')
        return

    logs = sender.send_eamil(sender.smpt['user'], receivers, subject, content)
    err_num = 0
    for log in logs:
        if log.status_code is None:
            err_num += 1

    if err_num != 0:
        print(f'共有{err_num}封邮件发送失败，请检查网络！')
    else:
        print('发送成功')

def bombard(sender):
    print('*******************************************')
    receiver = input('请输入收件人地址：')
    subject = input('请输入主题：')
    content = input('请输入内容（暂不支持复杂格式）：')

    while True:
        try:
            iterations = int(input('请输入轰炸次数：'))
        except Exception:
            print('输入有误，请重新输入：')
            continue

        error_num = 0
        for _ in range(iterations):
            log = sender.send_eamil(sender.smpt['user'], [receiver], subject, content)[0]
            if log.status_code is None:
                error_num += 1

        if error_num != 0:
            print(f'共有{error_num}封邮件发送失败，请检查网络！')
        else:
            print('轰炸完毕！')

        break

def main():
    print('*******************************************')
    print('欢迎使用邮件自动发送机(按住ctrl+C退出程序)')
    print('作者：Xianghao')
    print('目前仅支持office365邮箱')
    sender = login()

    while True:
        print('*******************************************')
        print('1.群发邮件 2.邮件轰炸（请慎用）q.退出')
        choice = input('请输入选择：')
        if choice == 'q':
            exit()
            
        try:
            choice_num = int(choice)
        except Exception:
            print('输入错误，请重新输入！')
            continue

        if choice_num == 1:
            group_email(sender)
        elif choice_num == 2:
            bombard(sender)
        else:
            print('输入错误，请重新输入！')
            continue

main()