from django.contrib import admin

from .models import Payment, Subscription, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "date_payment", "course", "lesson", "amount")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "course", "is_subscription")
