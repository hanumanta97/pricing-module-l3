from django.db import models
from django.contrib.auth.models import User

DAYS_OF_WEEK = [
    ('mon', 'Monday'), ('tue', 'Tuesday'), ('wed', 'Wednesday'),
    ('thu', 'Thursday'), ('fri', 'Friday'), ('sat', 'Saturday'), ('sun', 'Sunday'),
]

class PricingConfiguration(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    applicable_days = models.JSONField()  # e.g., ["mon", "wed"]
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class DistanceBasePrice(models.Model):
    config = models.ForeignKey(PricingConfiguration, on_delete=models.CASCADE)
    base_km = models.FloatField()
    price = models.FloatField()

class DistanceAdditionalPrice(models.Model):
    config = models.ForeignKey(PricingConfiguration, on_delete=models.CASCADE)
    price_per_km = models.FloatField()

class TimeMultiplierFactor(models.Model):
    config = models.ForeignKey(PricingConfiguration, on_delete=models.CASCADE)
    from_minute = models.IntegerField()
    to_minute = models.IntegerField()
    multiplier = models.FloatField()

class WaitingCharge(models.Model):
    config = models.ForeignKey(PricingConfiguration, on_delete=models.CASCADE)
    grace_period_minutes = models.IntegerField(default=3)
    charge_per_unit = models.FloatField()
    unit_minutes = models.IntegerField(default=3)

class ConfigChangeLog(models.Model):
    config = models.ForeignKey(PricingConfiguration, on_delete=models.CASCADE)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)