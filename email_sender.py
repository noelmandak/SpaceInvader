from kink import inject
import smtplib

@inject
class EmailSender:
    def __init__(self,email="noelmandak03@gmail.com",password="gqoizoewoxgqwprw"):
        self.Email_Address = email
        self.Email_Password = password
        smtp = smtplib.SMTP("smtp.gmail.com", 587)
        # smtp.ehlo()
        smtp.starttls()
        # smtp.ehlo()
        smtp.login(self.Email_Address, self.Email_Password)
        self.smtp = smtp

    def send(self, receiver, subject, body):
        try:
            msg = f"Subject: {subject}\n\n{body}"

            self.smtp.sendmail(self.Email_Address, receiver, msg)
            print("email terkirim")
        except:
            print("email gagal dikirim")

# sender = EmailSender()
# sub = "Percobaan"
# body = "so lapar kita"
# receiver = "jmspatrick77@gmail.com"

# sender.send(receiver,sub,body)