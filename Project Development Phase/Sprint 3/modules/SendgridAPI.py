from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class SendGridAPI:
    def __init__(self):
        self.sg = SendGridAPIClient('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')

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
        