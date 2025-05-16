from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PricingConfiguration, ConfigChangeLog
from threading import local

_user = local()

def set_actor(user):
    _user.value = user

def get_actor():
    return getattr(_user, 'value', None)

@receiver(post_save, sender=PricingConfiguration)
def log_config_change(sender, instance, created, **kwargs):
    user = get_actor()
    if not user:
        return
    action = "Created" if created else "Updated"
    ConfigChangeLog.objects.create(
        config=instance,
        changed_by=user,
        action=action
    )
