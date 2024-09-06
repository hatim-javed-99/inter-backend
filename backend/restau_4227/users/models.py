from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django_rest_passwordreset.signals import reset_password_token_created
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    def __str__(self):
        return self.username


class Profile(models.Model):
    USER_GENDER = [
        ('male', 'Male'),
        ('female', 'Female')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_profile")
    name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=6, choices=USER_GENDER, null=True, blank=True)
    phone = PhoneNumberField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='images', blank=True, null=True)
    address = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal receiver function to create a user profile when a new user is created.
    """
    if created:
        Profile.objects.create(user=instance)
    else:
        pass


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # send an e-mail to the user
    context = {
        'username': reset_password_token.user.get_full_name,
        'reset_password_token': reset_password_token.key
    }
    # render email text
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)
    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Final Year Project"),
        # message:
        email_plaintext_message,
        # from:
        "demo@gmail.com",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
