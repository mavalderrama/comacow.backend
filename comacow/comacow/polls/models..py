import uuid
from django.db import models
from django.contrib.auth.models import User

from .managers import UserManager


class Users(models.Model):
    USER_TYPES = [
        ('FR', 'Farmer'),
        ('BC', 'Big Customer'),
        ('MM', 'Middle Man'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nit = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    pwd = models.CharField(max_length=500)
    user_type = models.CharField(max_length=2, choices=USER_TYPES)
    phone = models.CharField(max_length=200)
    date_created = models.DateField(auto_now_add=True)

    objects = UserManager()

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Users.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class FarmOrder(models.Model):
    STATUS = [
        ("FS", "For Sale"),
        ("SD", "Sold"),
        ("NA", "Not Available")
    ]
    id_order = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_user = models.ForeignKey("User", on_delete=models.CASCADE)
    id_animal = models.ForeignKey("Livestock", on_delete=models.CASCADE)
    status = models.CharField(default=2, choices=STATUS)
    details = models.CharField(default=500)
