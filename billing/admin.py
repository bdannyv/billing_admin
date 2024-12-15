from django.contrib import admin

from .models import Action, ActionCode, Actor, Bill, Client, ClientPayer, Matter, Payer

# Register your models here.


class BillInline(admin.TabularInline):
    model = Bill
    exclude = ["id"]
    extra = 0


class ClientsPayersInline(admin.TabularInline):
    model = ClientPayer
    exclude = ["id"]
    extra = 0


class MatterInline(admin.TabularInline):
    model = Matter
    exclude = ["id"]
    extra = 0


class ActionInline(admin.TabularInline):
    model = Action
    exclude = ["id"]
    extra = 0


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    inlines = [ClientsPayersInline, MatterInline]
    exclude = ["id"]


@admin.register(Payer)
class PayerAdmin(admin.ModelAdmin):
    inlines = [ClientsPayersInline]
    exclude = ["id"]


@admin.register(Matter)
class MatterAdmin(admin.ModelAdmin):
    inlines = [ActionInline]
    exclude = ["id"]


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    inlines = [BillInline, ActionInline]
    exclude = ["id"]


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    inlines = [ActionInline]
    exclude = ["id"]


@admin.register(ActionCode)
class ActionCodeAdmin(admin.ModelAdmin):
    inlines = [ActionInline]
    exclude = ["id"]
