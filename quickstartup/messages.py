# coding: utf-8


from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template import RequestContext, TemplateDoesNotExist
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _


class SendMailException(Exception):
    pass


def send_transaction_mail(user, template_name, request=None, site=None,
                          template_base="emails/{}.{}",
                          subject_template_base="emails/{}-subject.html",
                          **context):
    if request is not None:
        site = get_current_site(request)

    context.update({'user': user, 'site': site})

    subject = render_to_string(subject_template_base.format(template_name, "html"), context)
    subject = ''.join(subject.splitlines())

    from_email = settings.DEFAULT_FROM_EMAIL
    message_txt = render_to_string(template_base.format(template_name, "txt"), context)
    email_message = EmailMultiAlternatives(subject, message_txt, from_email, [user.email])

    try:
        message_html = render_to_string(template_base.format(template_name, "html"), context)
    except TemplateDoesNotExist:
        pass
    else:
        email_message.attach_alternative(message_html, 'text/html')

    email_message.send(fail_silently=not settings.DEBUG)


def send_contact_mail(instance, created, **kwargs):
    if not created:
        return

    template = _(
        "Contact From: {instance.name} <{instance.email}>\n"
        "Phone: {instance.phone}\n"
        "Message:\n"
        "{instance.message}\n"
        "URL: http://{domain}{instance.admin_url}\n"
    )

    domain = settings.QS_PROJECT_DOMAIN
    email = EmailMessage(
        subject=_("New Contact from %s") % (settings.QS_PROJECT_NAME,),
        body=template.format(domain=domain, instance=instance),
        from_email=settings.QS_PROJECT_CONTACT,
        to=[settings.QS_PROJECT_CONTACT],
        headers={"Reply-To": instance.email},
    )

    email.send(fail_silently=not settings.DEBUG)
