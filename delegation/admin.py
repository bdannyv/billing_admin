from django.contrib import admin

from .models import UserActor

# Register your models here.


@admin.register(UserActor)
class UserActorAdmin(admin.ModelAdmin):
    exclude = ["id"]
