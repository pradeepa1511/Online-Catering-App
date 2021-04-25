from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Catering)
admin.site.register(Menu)
admin.site.register(Bill)
admin.site.register(orderItem)
