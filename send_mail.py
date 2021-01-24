from email.mime.text import MIMEText
import smtplib

def send_email(email, height, average_height, count):
    from_email= "adrianstark13@gmail.com"
    from_password="Windows15$$"
    to_email=email

    subject="Height data"
    message="Hi there, your height is <strong>%s</strong>. Average height of all <strong>%s</strong> participants is <strong>%s</strong>" %(height,count, average_height)

    msg=MIMEText(message, 'html') # converts the "message" variable to html
    msg['Subject']=subject
    msg['To']=to_email
    msg['From']=from_email

    gmail=smtplib.SMTP('smtp.gmail.com',587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email,from_password)
    gmail.send_message(msg)