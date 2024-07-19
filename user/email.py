from django.core.mail import send_mail, BadHeaderError
import logging

logger = logging.getLogger(__name__)

def send_activation_code(email, activation_code):
    '''
    Функция для отправки пользавателю активационного кода по имейлу

    email (str): Адрес электронной почты получателя.
    activation_code (str): Код активации для вставки в сообщение.

    subject - заголовок для активационного кода 
    messsage - сообщение где хранится данные где хранится код
    from email - от кого имейл
    reciptient_list - кому отправляем
    '''
    title = 'Account Activation'
    message = f'Thank you for signing up. Your activation code is {activation_code}'
    from_email = 'admin@admin.com'
    recipient_list = [email]

    try:
        send_mail(
            title,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )
        logger.info(f'Activation email sent to {email}')
    except BadHeaderError:
        logger.error('Invalid header found.')
    except ConnectionRefusedError:
        logger.error('Connection refused.')
    except Exception as e:
        logger.error(f'Error sending email: {str(e)}')