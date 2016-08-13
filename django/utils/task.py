from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template

from labcomp.celery import app


@app.task(name='send_mail')
def send_mail(recipient_list, subject, template_name, data):
    """
        Just send an email with Sparkpost (Sparkpost Template)
    :param subject: str
    :param recipient_list: list
    :param template_name: str
    :param data: dict
    :return:
    """

    html_content = get_template(template_name).render(Context(data))
    msg = EmailMultiAlternatives(subject, '', settings.ADMIN_MAIL, recipient_list)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
