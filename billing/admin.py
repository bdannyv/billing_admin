from django.contrib import admin

from delegation.models import UserActor

from .models import Action, ActionCode, Actor, Bill, Client, ClientPayer, Matter, Payer


class ActorDelegationViaUserInline(admin.TabularInline):
    model = UserActor
    extra = 0


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


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    exclude = ["id"]
    ordering = ["-created_at", "title"]
    search_fields = ["title"]


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    inlines = [ClientsPayersInline, MatterInline]
    exclude = ["id"]
    ordering = ["name", "-number"]
    search_fields = ["name", "number"]


@admin.register(Payer)
class PayerAdmin(admin.ModelAdmin):
    inlines = [ClientsPayersInline]
    exclude = ["id"]
    ordering = ["name", "-number"]
    search_fields = ["name", "number"]


@admin.register(Matter)
class MatterAdmin(admin.ModelAdmin):
    inlines = [ActionInline]
    exclude = ["id"]
    ordering = ["title", "-number"]
    search_fields = ["title", "number"]


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    inlines = [BillInline, ActionInline, ActorDelegationViaUserInline]
    exclude = ["id"]
    ordering = ["name"]
    search_fields = ["name", "number"]


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    inlines = [ActionInline]
    exclude = ["id"]
    ordering = ["-number"]
    search_fields = ["title", "number", "bill_actor"]


@admin.register(ActionCode)
class ActionCodeAdmin(admin.ModelAdmin):
    inlines = [ActionInline]
    exclude = ["id"]
    ordering = ["code"]
    search_fields = ["code", "classification", "description"]
