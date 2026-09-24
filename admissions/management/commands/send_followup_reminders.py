from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from admissions.models import Communication, FollowUp


class Command(BaseCommand):
    help = "Send due follow-up reminders to assigned staff and optionally to leads by WhatsApp/SMS"

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        now = timezone.now()
        candidates = FollowUp.objects.filter(completed=False, reminder_sent_at__isnull=True, due_at__gte=now - timedelta(minutes=5), due_at__lte=now + timedelta(days=1)).select_related("lead", "lead__assigned_to", "created_by")
        processed = 0
        for item in candidates:
            send_after = item.due_at - timedelta(minutes=item.reminder_minutes_before)
            if now < send_after: continue
            if options["dry_run"]:
                self.stdout.write(f"Would remind: {item.lead.name} at {item.due_at}"); continue
            results = []
            assigned = item.lead.assigned_to
            if item.notify_assignee_email:
                if assigned and assigned.email:
                    try:
                        send_mail(f"CRM follow-up due: {item.lead.name}", f"Hello {assigned.get_full_name() or assigned.username},\n\nYour CRM follow-up for {item.lead.name} ({item.lead.phone}) is due at {timezone.localtime(item.due_at):%d %b %Y, %I:%M %p}.\n\nTask: {item.note}\n\nOpen the College Admission CRM to update the lead.", settings.DEFAULT_FROM_EMAIL, [assigned.email], fail_silently=False)
                        results.append("Assignee email sent")
                    except Exception as exc: results.append(f"Assignee email failed: {exc}")
                else: results.append("Assignee email skipped: no assigned user/email")
            from admissions.views import deliver_communication
            message = f"Hello {item.lead.name}, reminder from College Admission: {item.note}. Scheduled for {timezone.localtime(item.due_at):%d %b, %I:%M %p}."
            for enabled, channel in [(item.notify_lead_whatsapp, "WhatsApp"), (item.notify_lead_sms, "SMS")]:
                if not enabled: continue
                communication = Communication.objects.create(lead=item.lead, channel=channel, message=message, status="Queued", created_by=item.created_by)
                deliver_communication(communication); results.append(f"{channel}: {communication.status}")
            item.reminder_sent_at, item.reminder_result = now, "; ".join(results) or "No notification channel selected"
            item.save(update_fields=["reminder_sent_at", "reminder_result"]); processed += 1
        self.stdout.write(self.style.SUCCESS(f"Processed {processed} follow-up reminder(s)."))
