from django.contrib import admin
from .models import ListCurrency, ListBalanceCalcMethod, ListCustomer, ListGood, AdvUser
import datetime
from .utilities import send_activation_notification


def send_activation_notifications(modeladmin, request, queryset):
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)


# Register your models here.
admin.site.register(ListCustomer)
admin.site.register(ListBalanceCalcMethod)
admin.site.register(ListCurrency)
admin.site.register(ListGood)
admin.site.register(AdvUser)

admin.site.index_title = 'Администратор сахифаси'
admin.site.site_header = 'Сайтни бошқариш'
admin.site.site_title = 'Tillayev LAB'
