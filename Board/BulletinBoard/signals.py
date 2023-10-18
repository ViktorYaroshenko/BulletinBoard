from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ad, Response
from django.core.mail import send_mail, mail_admins
from django.contrib.auth.models import User


@receiver(post_save, sender=Response)
def send_mail_resp(sender, instance, created, **kwargs):
    if created:
        user = Ad.objects.get(pk=instance.resp_ad_id).author
        to_email = user.email
        send_mail(
            subject='Новый отклик',
            message=f'{instance.resp_author} оставил такой отклик на одно из Ваших объявлений: {instance.text}',
            from_email="79854550554@mail.ru",
            recipient_list=[to_email,],
        )

# @receiver(post_save, sender=Response)
# def send_mail_admins(sender, instance, created, **kwargs):
#     if created:
#         mail_admins(subject="1234", message = "Новый респонсище")
