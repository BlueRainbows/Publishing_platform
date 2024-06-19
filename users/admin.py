from django.contrib import admin
from users.models import User, Subscription

admin.site.register(User)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_data',)
