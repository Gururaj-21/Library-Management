from django.core.mail import send_mail
from django.conf import settings

def send_email(password,recipient_mail):
    subject = 'Library Application Password'
    message = f'''Hi,
                 we have attached the password below. Please find it.
                 {password}
                 Thank You,
               '''
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [].append(recipient_mail)

    send_mail(subject, message, email_from, recipient_list)


