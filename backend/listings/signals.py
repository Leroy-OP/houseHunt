import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Property, Booking
from notifications.models import Notification

logger = logging.getLogger(__name__)
User = get_user_model()


@receiver(post_save, sender=Property)
def property_created_notification(sender, instance, created, **kwargs):
    if not created:
        return

    try:
        all_users = User.objects.all()

        Notification.objects.bulk_create([
            Notification(
                user=user,
                type='listing',                        # ← was notification_type
                title='New Property Listed',
                body=f'A new property "{instance.title}" is now available.',
            )
            for user in all_users
        ])

        logger.info(
            "Listing notifications created for %s users (property %s).",
            all_users.count(), instance.pk,
        )

    except Exception:
        logger.exception(
            "property_created_notification failed for Property pk=%s", instance.pk
        )


@receiver(post_save, sender=Booking)
def booking_notification(sender, instance, created, **kwargs):
    if not created:
        return

    try:
        prop        = instance.property if instance.property_id else None
        agency_user = prop.agency.user if prop and prop.agency_id and prop.agency else None
        tenant_name = (
            instance.tenant.get_full_name() or instance.tenant.username
            if instance.tenant_id and instance.tenant
            else "Unknown tenant"
        )

        if not agency_user:
            logger.warning("booking_notification: Booking %s has no agency user, skipping.", instance.pk)
            return

        Notification.objects.create(
            user=agency_user,
            type='booking',                            # ← was notification_type
            title='New Booking Request',
            body=f'"{tenant_name}" has requested to book "{prop.title}".',
        )

    except Exception:
        logger.exception("booking_notification failed for Booking pk=%s", instance.pk)