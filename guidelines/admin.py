from django.contrib import admin

from .models import (
    Guideline,
    GuidelineActor,
    GuidelineClient,
    GuidelineMatter,
    GuidelinePayer,
    Rule,
    RuleActor,
    RuleClient,
    RuleMatter,
    RulePayer,
)

# Register your models here.


class RuleInline(admin.TabularInline):
    model = Rule
    extra = 0


class GPayerInline(admin.TabularInline):
    model = GuidelinePayer
    extra = 0


class RPayerInline(admin.TabularInline):
    model = RulePayer
    extra = 0


class GMatterInline(admin.TabularInline):
    model = GuidelineMatter
    extra = 0


class RMatterInline(admin.TabularInline):
    model = RuleMatter
    extra = 0


class GClientInline(admin.TabularInline):
    model = GuidelineClient
    extra = 0


class RClientInline(admin.TabularInline):
    model = RuleClient
    extra = 0


class GActorInline(admin.TabularInline):
    model = GuidelineActor
    extra = 0


class RActorInline(admin.TabularInline):
    model = RuleActor
    extra = 0


@admin.register(Guideline)
class GuidelineAdminModel(admin.ModelAdmin):
    inlines = [RuleInline, GPayerInline, GClientInline, GMatterInline, GActorInline]
    exclude = ["id"]


@admin.register(Rule)
class RuleAdminModel(admin.ModelAdmin):
    inlines = [RPayerInline, RClientInline, RMatterInline, RActorInline]
    exclude = ["id"]
