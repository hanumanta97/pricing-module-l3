from django.contrib import admin
from .models import *
from .signals import set_actor

class DistanceBasePriceInline(admin.TabularInline):
    model = DistanceBasePrice
    extra = 1

class DistanceAdditionalPriceInline(admin.TabularInline):
    model = DistanceAdditionalPrice
    extra = 1

class TimeMultiplierFactorInline(admin.TabularInline):
    model = TimeMultiplierFactor
    extra = 1

class WaitingChargeInline(admin.TabularInline):
    model = WaitingCharge
    extra = 1

@admin.register(PricingConfiguration)
class PricingConfigurationAdmin(admin.ModelAdmin):
    inlines = [DistanceBasePriceInline, DistanceAdditionalPriceInline, TimeMultiplierFactorInline, WaitingChargeInline]
    list_display = ('name', 'is_active', 'created_at')

    def save_model(self, request, obj, form, change):
        set_actor(request.user)
        super().save_model(request, obj, form, change)

@admin.register(ConfigChangeLog)
class ConfigChangeLogAdmin(admin.ModelAdmin):
    list_display = ('config', 'changed_by', 'action', 'timestamp')

