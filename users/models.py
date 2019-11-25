from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string


class User(AbstractUser):

    """ Custom User Model """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHERS = "others"

    LANGUAGE_KOREAN = "kr"
    LANGUAGE_ENGLISH = "en"

    CURRENCY_KRW = "kr"
    CURRENCY_USD = "us"

    AUTH_EMAIL = "Email"
    AUTH_GITHUB = "Github"
    AUTH_KAKAO = "Kakao"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHERS, "Others"),
    )
    LANGUAGE_CHOICES = ((LANGUAGE_KOREAN, "Korean"), (LANGUAGE_ENGLISH, "English"))
    CURRENCY_CHOICES = ((CURRENCY_KRW, "KRW"), (CURRENCY_USD, "USD"))
    AUTH_CHOICES = (
        (AUTH_EMAIL, "Email"),
        (AUTH_GITHUB, "Github"),
        (AUTH_KAKAO, "Kakao"),
    )

    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    language = models.CharField(
        max_length=2, choices=LANGUAGE_CHOICES, blank=True, default=LANGUAGE_ENGLISH
    )
    currency = models.CharField(
        max_length=2, choices=CURRENCY_CHOICES, blank=True, default=CURRENCY_USD
    )
    avatar = models.ImageField(upload_to="avatars", blank=True)
    bio = models.TextField(blank=True)
    superhost = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=120, default="", blank=True)
    auth = models.CharField(max_length=40, choices=AUTH_CHOICES, default=AUTH_EMAIL)

    def verify_email(self):

        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret

            SUBJECT = "Verify Email"
            FROM = settings.EMAIL_FROM
            TO_LIST = [self.email]
            HTML_MESSAGE = render_to_string("verification.html", {"secret": secret})
            MESSAGE = strip_tags(HTML_MESSAGE)
            send_mail(
                SUBJECT,
                MESSAGE,
                FROM,
                TO_LIST,
                fail_silently=False,
                html_message=HTML_MESSAGE,
            )
            self.save()
        return
