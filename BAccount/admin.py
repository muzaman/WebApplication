from django.contrib import admin
from .models import ListCurrency, ListBalanceCalcMethod, ListCustomer, ListGood, AdvUser
import datetime
from .utilities import send_activation_notification


def send_activation_notifications(modeladmin, request, queryset):
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)
    modeladmin.message_user(request, 'Тасдиқ хатлари юборилди')


send_activation_notifications.short_description = 'Фаоллаштириш тасдиқ хатларини юбориш'


class NonactivatedFilter(admin.SimpleListFilter):
    title = 'Фаоллаштиришдан ўтилдими?'
    parameter_name = 'actstate'

    def lookups(self, request, model_admin):
        return (
            ('activated', 'ўтилди'),
            ('threedays', '3 кундан кўпроқ вақтда ўтмади'),
            ('week', 'Бир хафтадан кўпроқ вақтда ўтмади')
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val == 'activated':
            return queryset.filter(is_active=True, is_activated=True)
        elif val == 'threedays':
            d = datetime.date.today() - datetime.timedelta(days=3)
            return queryset.filter(
                is_active=False, is_activated=False,
                date_joined__date__lt=d)
        elif val == 'week':
            d = datetime.date.today() - datetime.timedelta(weeks=1)
            return queryset.filter(
                is_active=False, is_activated=False,
                date_joined__date__lt=d)


class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_activated', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = (NonactivatedFilter,)
    fields = (('username', 'email'), ('first_name', 'last_name'),
              ('send_messages', 'is_active', 'is_activated'),
              'is_superuser',
              'groups', 'user_permissions',
              ('last_login', 'date_joined'))
    readonly_fields = ('last_login', 'date_joined')
    actions = (send_activation_notifications,)


admin.site.register(AdvUser, AdvUserAdmin)
# Register your models here.
admin.site.register(ListCustomer)
admin.site.register(ListBalanceCalcMethod)
admin.site.register(ListCurrency)
admin.site.register(ListGood)

admin.site.index_title = 'Администратор сахифаси'
admin.site.site_header = 'Сайтни бошқариш'
admin.site.site_title = 'Tillayev LAB'
