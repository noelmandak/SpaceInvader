import smtplib

class EmailSender:
    def __init__(self,email="noelmandak03@gmail.com",password="gqoizoewoxgqwprw"):
        self.Email_Address = email
        self.Email_Password = password
        smtp = smtplib.SMTP("smtp.gmail.com", 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(self.Email_Address, self.Email_Password)
        self.smtp = smtp

    def send(self, receiver, subject, body):

            msg = f"Subject: {subject}\n\n{body}"

            self.smtp.sendmail(self.Email_Address, receiver, msg)
            print("email terkirim")

sender = EmailSender()
sub = "Hooo"
body = "so lapar kita"
receiver = "nmandak36@students.calvin.ac.id"

sender.send(receiver,sub,body)