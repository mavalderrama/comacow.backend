from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(User, UserAdmin)
admin.site.register(Livestock)
admin.site.register(Farm)
admin.site.register(FarmOrder)
admin.site.register(MiddlemanOrder)
admin.site.register(CustomerOrder)
