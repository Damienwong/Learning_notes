#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: haibo.wang
@Date: 2025/7/27
@Description: 
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
from email.utils import formataddr
import os


class MyEmail:
    def __init__(self, smtp_server, smtp_port, username, password, use_ssl=True):
        """
        初始化邮件发动器
        :param smtp_server: SMTP服务器地址
        :param smtp_port: SMTP服务器端口
        :param username: 邮箱用户名
        :param password: 邮箱密码/授权码
        :param use_ssl: 是否使用SSL加密连接
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.use_ssl = use_ssl

    def _connect(self):
        """
        建立SMTP连接
        """
        if self.use_ssl:
            server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
        else:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()

        server.login(self.username, self.password)
        return server

    def send_email(self, subject, content, to_addrs, content_type='plain', attachments=None, from_name=None):
        """
        发送邮件
        :param subject: 邮件主题
        :param content: 邮件内容
        :param to_addrs: 收件人地址，单个字符或列表
        :param content_type: 内容类型 plain->文本，html->网页
        :param attachments: 附件路径列表
        :param from_name: 发件人显示名称
        """
        # 处理收件人格式
        if isinstance(to_addrs, str):
            to_addrs = [to_addrs]

        # 创建邮件基础结构
        if attachments:
            msg = MIMEMultipart
        else:
            msg = MIMEText(content, content_type, 'utf-8')

        # 设置邮件头部
        if from_name:
            # 格式：发件人名称<发件人邮箱>
            msg['From'] = formataddr((str(Header(from_name, 'utf-8')), self.username))
        else:
            msg['From'] = self.username

        msg['To'] = Header(','.join(to_addrs))
        msg['Subject'] = Header(subject, 'utf-8')

        # 添加附件
        if attachments:
            # 添加正文
            msg.attach(MIMEText(content, content_type, 'utf-8'))

            # 添加所有附件
            for file_path in attachments:
                if not os.path.isfile(file_path):
                    raise FileNotFoundError(f'附件不存在: {file_path}')

                with open(file_path, 'rb') as f:
                    file_data = f.read()
                    file_name = os.path.basename(file_path)
                    attachment = MIMEApplication(file_data)
                    attachment.add_header(
                        'Content-Disposition',
                        'attachment',
                        file_name=(Header(file_name, 'utf-8').encode())
                    )
                    msg.attach(attachment)

        # 发送邮件
        try:
            # with self._connect() as server:
            server = self._connect()
            server.sendmail(self.username, to_addrs, msg.as_string())
            print('邮件发送成功')
        except smtplib.SMTPDataError as e:
            error_code = e.smtp_code
            error_message = e.smtp_error.decode('utf-8')
            raise Exception(f'邮件发送失败(错误代码:{error_code}): {error_message}') from e
        finally:
            if 'server' in locals():
                try:
                    server.quit()
                except:
                    try:
                        server.close()
                    except:
                        pass

    def send_text(self, subject, text, to_addrs, from_name=None):
        self.send_email(subject, text, to_addrs, 'plain', None, from_name)

    def send_html(self, subject, html, to_addrs, from_name=None):
        self.send_email(subject, html, to_addrs, 'html', None, from_name)

    def send_attachment(self, subject, content, to_addrs, content_type, attachments, from_name):
        self.send_email(subject, content, to_addrs, content_type, attachments, from_name)


if __name__ == '__main__':
    myemail = MyEmail(
        smtp_server='smtp.qq.com',
        smtp_port=465,
        username='454671404@qq.com',
        password='erouqkyzcqwfbjca',
        use_ssl=True
    )

    myemail.send_text(
        subject='Test_Mail_Sending_Func',
        text='This is a testing mail',
        to_addrs='haibonewang@126.com',
        from_name='王海波的QQ邮箱'
    )

