from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import UserActor

# Register your models here.


class DelegationInlines(admin.TabularInline):
    model = UserActor
    extra = 1


@admin.register(UserActor)
class UserActorAdmin(admin.ModelAdmin):
    exclude = ["id"]


admin.site.unregister(
    User,
)


@admin.register(User)
class UserAdminCustom(UserAdmin):
    inlines = [DelegationInlines, *UserAdmin.inlines]
