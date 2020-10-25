import smtplib
from email_service import credential
from email.message import EmailMessage

EMAIL_ADDRESS = credential.EMAIL_ADDRESS
EMAIL_PASSWORD = credential.EMAIL_PASSWORD


def send_mail(receivers_list, subject, body):
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg.set_content(body)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            msg['To'] = ','.join(receivers_list)
            smtp.send_message(msg)
        return True
    except:
        return False


if __name__ == '__main__':
    send_mail(["aminulhaq785@gmail.com", "bmqube1@gmail.com"], "Welcome", "Hello from PScamp, sent from python script.")
