import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import yaml


class CustomEmail:
    def __init__(self):
        self.content = ""
        self.empty = True
        with open("config.yaml") as f:
            config = yaml.safe_load(f)
        email = config['EMAIL']
        self.sender_email = email['USER']
        self.receiver_email = email['RECEIVER_EMAIL']
        self.password = email['PASSWORD']
        self.smtp_server = email['SMTP_SERVER']
        self.smtp_port = email['PORT']
        self.access_url = config['SERVER']['PUBLIC_URL']

    def add_header(self, header):
        self.content += "<h2>{}</h2><br>".format(header)

    def add_article(self, site, url, article_version, changed_count):
        self.empty = False
        self.content += "<a href=\"{url}\">{headline}</a> has now been <a href=\"{ndurl}\">changed</a> {times} time(s) ({percent}%)<br><br>".format(
            url=url, headline=article_version.headline, times=changed_count, ndurl=self.access_url + site + "/" + url, percent=str(int(article_version.total_similarity*100)))

    def send(self):
        message = MIMEMultipart("alternative")
        message["Subject"] = "NewsDiffs update!"
        message["From"] = self.sender_email
        message["To"] = self.receiver_email
        html = MIMEText(self.content, "html")
        message.attach(html)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(
                self.sender_email, self.receiver_email, message.as_string()
            )