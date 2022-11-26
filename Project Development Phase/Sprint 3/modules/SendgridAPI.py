import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class SendgridAPI:
    def __init__(self):
        self.sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))]

    def send(self, to_email, subject, content):
        message = Mail(from_email='smartstockoffi@gmail.com',
                       to_emails=to_email,
                       subject=subject,
                       html_content=content)
        try:
            response = self.sg.send(message)
            return True
        except:
            return False

SG = SendgridAPI()
SG.send('ganappriyanc@gmail.com', 'Test', 'Test')