from django.contrib import admin

from .models import Counterparty, Upd, Service, Payment, Object, ObjectGroup


class CounterpartyAdmin(admin.ModelAdmin):
    list_display = ('inn', 'name', 'time_create')
    list_display_links = ('inn', 'name')
    search_fields = ('inn', 'name')


class ObjectGroupAdmin(admin.ModelAdmin):
    list_display = ('group', 'object', 'fee')
    list_display_links = ('group', 'object', 'fee')


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('counterparty', 'object', 'amount', 'date', 'time_create')
    list_display_links = ('counterparty', 'object')
    search_fields = ('counterparty__name',)


class ServiceInline(admin.TabularInline):
    model = Service


class UpdAdmin(admin.ModelAdmin):
    inlines = [
        ServiceInline,
    ]
    list_display = ('number', 'counterparty', 'date', 'time_create')
    search_fields = ('counterparty__name', 'number')


admin.site.register(Counterparty, CounterpartyAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Object)
admin.site.register(ObjectGroup, ObjectGroupAdmin)
admin.site.register(Upd, UpdAdmin)
