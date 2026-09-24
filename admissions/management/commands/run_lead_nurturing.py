from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from admissions.models import Communication, FollowUp, Lead, NurtureLog

MESSAGES = {
    1: "Welcome to College Admission. We provide transparent course, college and application guidance. Your counsellor will contact you shortly.",
    3: "Explore suitable colleges, fee structures and scholarship opportunities with your College Admission counsellor.",
    7: "Admission reminder: seat availability changes quickly. Reply to receive the latest options for your preferred course.",
    15: "Important admission date reminder: complete pending documents and application steps before the last date.",
    30: "Still planning admission? Reply to restart your free counselling and receive an updated college shortlist.",
}

class Command(BaseCommand):
    help = "Run consent-based Day 1, 3, 7, 15 and 30 lead nurturing"
    def handle(self, *args, **options):
        now=timezone.now(); processed=0
        for lead in Lead.objects.filter(consent=True).exclude(status__in=["Admission Confirmed","Registered","Closed","Lost"]).select_related("assigned_to"):
            age=(now.date()-lead.created_at.date()).days
            for day,message in MESSAGES.items():
                if age < day or NurtureLog.objects.filter(lead=lead,day=day).exists(): continue
                results=[]
                for channel in ["Email","WhatsApp","SMS"]:
                    if channel == "Email" and not lead.email: continue
                    item=Communication.objects.create(lead=lead,channel=channel,subject=f"College Admission Day {day} Update" if channel=="Email" else "",message=message,status="Queued")
                    from admissions.views import deliver_communication
                    deliver_communication(item); results.append(f"{channel}:{item.status}")
                if day==1 and not FollowUp.objects.filter(lead=lead,completed=False).exists():
                    FollowUp.objects.create(lead=lead,due_at=now+timedelta(hours=2),note="First counsellor welcome call",created_by=lead.assigned_to)
                    results.append("Counsellor call scheduled")
                statuses=[x.split(":")[-1] for x in results if ":" in x]
                state="Sent" if statuses and all(x=="Sent" for x in statuses) else "Partial" if "Sent" in statuses else "Failed"
                NurtureLog.objects.create(lead=lead,day=day,status=state,details="; ".join(results)); processed+=1
        self.stdout.write(self.style.SUCCESS(f"Processed {processed} nurturing step(s)."))
