from django.conf import settings
from .models import College, Course, SiteSettings, SocialLink
from .forms import LeadForm

def portal_links(request):
    settings_obj, _ = SiteSettings.objects.get_or_create(pk=1)
    return {
        "social_links": SocialLink.objects.filter(active=True).exclude(url="").order_by("display_order", "platform"),
        "whatsapp_number": settings.WHATSAPP_NUMBER,
        "portal_settings": settings_obj,
        "popup_courses": Course.objects.all().order_by("name"),
        "popup_colleges": College.objects.filter(active=True).order_by("name"),
        "apply_form": LeadForm(),
    }
