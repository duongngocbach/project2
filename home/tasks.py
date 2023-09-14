from celery import shared_task
import smtplib 
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


# @shared_task
# def add(x, y):
#     return x + y 

username = "bachdn3@fpt.com.vn" 
password = "devKTHT@123456"
mail_server = 'mail.fpt.com.vn'
to_emails = ["ngocbach99ltv@gmail.com"] 
cc_emails = []

def handle_base_email(message,
                      to_emails,
                      cc_emails):
    server = smtplib.SMTP(mail_server, 587)
    server.starttls()
    server.login(username, password)
    to_adds = to_emails + cc_emails
    server.sendmail(username, to_adds, message)
    server.close()
 
 
def handle_report_email(to_emails,
                        cc_emails,
                        subject,
                        html_text,
                        images = [],
                        files = []):
    message = MIMEMultipart('mixed')
    message['Subject'] = subject
    message['From'] = username
    message['To'] = ','.join(to_emails)
    message['Cc'] = ','.join(cc_emails)
 
    message.preamble = 'This is a multi-part message in MIME format.'
 
    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    message.attach(msgAlternative)
 
    msgText = MIMEText('This is the alternative plain text message.')
    msgAlternative.attach(msgText)
 
    # We reference the image in the IMG SRC attribute by the ID we give it below
    msgText = MIMEText(html_text, 'html')
    
    msgAlternative.attach(msgText)

    for image in images:
    # This example assumes the image is in the current directory
      fp = open(image, 'rb')
      msgImage = MIMEImage(fp.read())
      fp.close()
      msgImage.add_header('Content-ID', f'<image{images.index(image) + 1}>')
      message.attach(msgImage)

    for file in files:
      with open(file, 'rb') as f:
          text_1 = f.read()
          attached_file_1 = MIMEApplication(text_1, _subtype='pdf')
          attached_file_1.add_header('content-disposition', 'attachment', filename=file)
          message.attach(attached_file_1)
 
 
    handle_base_email(message=message,
                      to_emails=to_emails,
                      cc_emails=cc_emails)


@shared_task
def send_email():
    handle_base_email("check celery", to_emails, cc_emails) 