from django.contrib import admin

from .models import *

admin.site.register(Counterparty)
admin.site.register(Upd)
admin.site.register(Service)
admin.site.register(Payment)
admin.site.register(Object)
admin.site.register(ObjectGroup)