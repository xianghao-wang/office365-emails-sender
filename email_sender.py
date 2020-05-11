import emails
from emails.template import JinjaTemplate as T

class EmailSender:
    def __init__(self, smpt_sonfig):
        self.smpt = smpt_sonfig

    @classmethod
    def default(cls, user_name, password):
        sender = cls({'host': 'smtp.office365.com',
             'user': user_name,
             'password': password,
             'port': 587,
             'tls': True})

        return sender

    def verificate(self):
        status = self.send_eamil('验证邮箱', [self.smpt['user']], '邮箱验证', '邮箱验证成功！')[0].status_code
        return status is not None


    def send_eamil(self, sender_nick_name, receivers, subject, content):
        user_name = self.smpt['user']
        message = emails.html(subject=T(subject),
                          html=T(content),
                          mail_from=(sender_nick_name, user_name)) 

        logs = []
        for receiver in receivers:
            print('发送中：' + receiver + '.....')
            history = message.send(to=(None, receiver), smtp=self.smpt)
            logs.append(history)

        return logs

