import uuid
from django.db import models
from django.contrib.auth.models import User


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

    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     '''
    #     Sends an email to this User.
    #     '''
    #     send_mail(subject, message, from_email, [self.email], **kwargs)


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Users.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()



class Farm(models.Model):
    id_farm = models.PositiveIntegerField(primary_key=True)
    n_cow = models.PositiveIntegerField()
    n_bull = models.PositiveIntegerField()
    n_calf = models.PositiveIntegerField()
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id_farm)


class Livestock(models.Model):
    ANIMAL = [
        ("CW", "Cow"),
        ("BL", "Bull"),
        ("CL", "Calf")
    ]
    STATUS = [
        ("FS", "For Sale"),
        ("SD", "Sold"),
        ("NA", "Not Available")
    ]
    id_animal = models.AutoField(primary_key=True)
    chapeta = models.CharField(max_length=264)
    animal_type = models.CharField(max_length=2, choices=ANIMAL)
    status = models.CharField(max_length=2, choices=STATUS)
    id_farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    raze = models.CharField(max_length=264)
    weight = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.chapeta


class FarmOrder(models.Model):
    STATUS = [
        ("FS", "For Sale"),
        ("SD", "Sold"),
        ("NA", "Not Available")
    ]
    id_order = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_animal = models.ForeignKey(Livestock, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=STATUS)
    details = models.CharField(max_length=500)


class MiddlemanOrder(models.Model):
    id_order = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=264)
    details = models.CharField(max_length=264)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_animal = models.ForeignKey(Livestock, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.status)


class CustomerOrder(models.Model):
    id_order = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=264)
    details = models.CharField(max_length=264)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_animal = models.ForeignKey(Livestock, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id_order)
