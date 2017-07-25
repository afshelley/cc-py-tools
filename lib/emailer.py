import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.load_config import Config

"""
    Emailer class
"""


class Emailer(Config):

    def __init__(self):
        super(Emailer, self).__init__()
        self._host = self.config['email']['host']
        self._port = self.config['email']['port']
        self._email = self.config['email']['email']
        self._password = self.config['email']['password']

    def send_email(self, **kwargs):
        """

        :param kwargs: see below

        :Keyword Arguments:
            subject (str): The title line of the email (default blank)
            body (str): The body text of the email (default blank)
            html (boolean): If True, tells the emailer to parse the body text as HTML (default False)
            recipients (str): An array of each recipient email address (default blank)
            sender (str): Changes the name of the sender in the email header (default same as the mailing address)
        """
        
        options = {
            'subject': '',
            'body': '',
            'html': False,
            'recipients': '',
            'sender': self._email
        }
        options.update(kwargs)

        msg = MIMEMultipart('alternative')
        msg['Subject'] = options['subject']
        msg['From'] = self._email
        msg['To'] = ", ".join(options['recipients'])

        if options['html']:
            body = MIMEText(options['body'], 'html')
        else:
            body = MIMEText(options['body'])

        msg.attach(body)
        receivers = options['recipients']

        smtp = smtplib.SMTP(host=self._host, port=self._port)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(self._email, self._password)
        smtp.sendmail(options['sender'], receivers, msg.as_string())
