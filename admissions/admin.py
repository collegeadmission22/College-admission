from django.contrib import admin
from django import forms
from .models import BulkDataBatch, CRMApiKey, ChatMessage, College, CollegeCategory, Communication, CommunicationTemplate, ContactMessage, Course, FollowUp, Lead, LeadActivity, LeadImportBatch, LeadRemark, NurtureLog, OnlineCourse, SiteSettings, SocialClick, SocialLink, StudentApplication, StudentDocument, StudentNotification, StudentPayment, UserProfile

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "course", "status", "source", "assigned_to", "uploaded_by", "created_at")
    list_filter = ("status", "source", "course", "assigned_to", "uploaded_by")
    search_fields = ("name", "phone", "email")
class CollegeAdminForm(forms.ModelForm):
    # College categories are selected directly from the CollegeCategory master.
    class Meta:
        model = College
        exclude = ("college_type", "courses")
        widgets = {
            "categories": forms.CheckboxSelectMultiple,
        }

    def save(self, commit=True):
        obj = super().save(commit=False)
        if commit:
            obj.save()
            self.save_m2m()
            # Keep the legacy college_type value populated for older frontend code.
            first = obj.categories.first()
            if first and obj.college_type != first.name[:30]:
                obj.college_type = first.name[:30]
                obj.save(update_fields=["college_type"])
        return obj


class CollegeCategoryMasterFilter(admin.SimpleListFilter):
    title = "College Category"
    parameter_name = "college_category_master"

    def lookups(self, request, model_admin):
        return [(str(c.pk), c.name) for c in CollegeCategory.objects.all().order_by("name")]

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        category = CollegeCategory.objects.filter(pk=self.value()).first()
        if not category:
            return queryset
        return queryset.filter(categories=category).distinct()


@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    form = CollegeAdminForm
    list_display = ("name", "university", "state", "country", "college_category_name")
    list_filter = ("university", "state", "country", CollegeCategoryMasterFilter)
    search_fields = ("name", "university__name", "state__name", "country__name")
    fieldsets = (
        ("College", {"fields": ("name", "university", "state", "country", "categories")}),
        ("Career content", {"fields": ("short_description", "description", "motivation")}),
        ("Upload College Image", {"fields": ("image",)}),
        ("SEO", {"fields": ("seo_title", "seo_description", "seo_keywords", "seo_slug")}),
    )

    @admin.display(description="College Category")
    def college_category_name(self, obj):
        return ", ".join(obj.categories.values_list("name", flat=True)) or obj.college_type

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "college_categories_display", "course_categories_display", "level", "duration")
    list_filter = ("college_categories", "course_categories", "level")
    search_fields = ("name",)
    filter_horizontal = ("college_categories", "course_categories")
    fieldsets = (
        ("Course", {"fields": ("name", "college_categories", "course_categories", "level", "duration")}),
        ("Career content", {"fields": ("short_description", "career_description", "motivation")}),
        ("Upload Course Image", {"fields": ("image",)}),
        ("SEO", {"fields": ("seo_title", "seo_description", "seo_keywords", "seo_slug")}),
    )

    @admin.display(description="College Categories")
    def college_categories_display(self, obj):
        return ", ".join(obj.college_categories.values_list("name", flat=True))

    @admin.display(description="Course Categories")
    def course_categories_display(self, obj):
        return ", ".join(obj.course_categories.values_list("name", flat=True))

class DocumentInline(admin.TabularInline):
    model = StudentDocument
    extra = 0

@admin.register(StudentApplication)
class StudentApplicationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "course", "college", "status", "updated_at")
    list_filter = ("status", "course", "college")
    search_fields = ("full_name", "phone", "email")
    inlines = [DocumentInline]

@admin.register(OnlineCourse)
class OnlineCourseAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "provider", "featured", "active")
    list_filter = ("category", "featured", "active")
    search_fields = ("title", "provider", "short_description", "description", "motivation")
    fieldsets = (
        ("Online Course", {"fields": ("title", "category", "provider", "specialization", "duration", "fee")}),
        ("Presentation Content", {"fields": ("short_description", "description", "motivation")}),
        ("Academic Details", {"fields": ("eligibility", "accreditation", "exam_mode", "lms_details")}),
        ("Links & Picture", {"fields": ("image", "external_image_url", "image_source_url", "external_url", "application_url", "brochure_url")}),
        ("SEO & Display", {"fields": ("seo_title", "seo_description", "seo_keywords", "seo_slug", "featured", "active")}),
    )

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("platform", "page_name", "url", "active", "display_order")
    list_editable = ("active", "display_order")

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("short_question", "session_key", "created_at")
    readonly_fields = ("session_key", "user_message", "bot_response", "created_at")
    def short_question(self, obj): return obj.user_message[:60]

admin.site.register([FollowUp, LeadActivity, LeadRemark, NurtureLog, StudentPayment, StudentNotification, ContactMessage, SocialClick])

@admin.register(CRMApiKey)
class CRMApiKeyAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "prefix", "active", "expires_at", "last_used_at", "created_at")
    list_filter = ("active", "created_at")
    readonly_fields = ("prefix", "key_hash", "created_by", "created_at", "last_used_at")

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "organisation", "college", "can_import_leads", "can_export_leads", "active")
    list_filter = ("role", "active", "can_import_leads", "can_export_leads")
    search_fields = ("user__username", "user__first_name", "user__last_name", "organisation")

@admin.register(LeadImportBatch)
class LeadImportBatchAdmin(admin.ModelAdmin):
    list_display = ("file_name", "uploaded_by", "assigned_to", "total_rows", "created_count", "updated_count", "rejected_count", "created_at")
    readonly_fields = ("uploaded_by", "file_name", "assigned_to", "total_rows", "created_count", "updated_count", "rejected_count", "error_report", "created_at")

@admin.register(BulkDataBatch)
class BulkDataBatchAdmin(admin.ModelAdmin):
    list_display = ("dataset", "file_name", "mode", "uploaded_by", "total_rows", "created_count", "updated_count", "skipped_count", "rejected_count", "imported_image_count", "created_at")
    list_filter = ("dataset", "mode", "created_at")
    readonly_fields = ("dataset", "mode", "file_name", "uploaded_by", "total_rows", "created_count", "updated_count", "skipped_count", "rejected_count", "imported_image_count", "error_report", "created_at")

@admin.register(Communication)
class CommunicationAdmin(admin.ModelAdmin):
    list_display = ("lead", "channel", "status", "created_by", "created_at", "sent_at")
    list_filter = ("channel", "status", "created_at")
    search_fields = ("lead__name", "lead__phone", "subject", "message")
    readonly_fields = ("provider_message_id", "provider_response", "created_at", "sent_at")

admin.site.register(CommunicationTemplate)

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (("Branding", {"fields": ("header_logo", "logo_alt_text")}), ("Apply Popup", {"fields": ("apply_popup_enabled", "auto_open_popup", "popup_title", "popup_message", "popup_delay_seconds")}),)
    def has_add_permission(self, request): return not SiteSettings.objects.exists()
    def has_delete_permission(self, request, obj=None): return False

# Modular CRM administration
from .models import ModuleAccess, EntranceExam, Classroom, SocialSEOItem, EmployeeRecord, CRMTask
for modular_model in [ModuleAccess, EntranceExam, Classroom, SocialSEOItem, EmployeeRecord, CRMTask]:
    try: admin.site.register(modular_model)
    except admin.sites.AlreadyRegistered: pass

# Admissions Administration master data: each item supports Add / Change / Delete.
from .models import CountryMaster, StateMaster, UniversityMaster, CourseCategoryMaster

@admin.register(CountryMaster)
class CountryMasterAdmin(admin.ModelAdmin):
    list_display = ("name", "active")
    list_editable = ("active",)
    search_fields = ("name",)

@admin.register(StateMaster)
class StateMasterAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "active")
    list_filter = ("country", "active")
    list_editable = ("active",)
    search_fields = ("name", "country__name")

@admin.register(UniversityMaster)
class UniversityMasterAdmin(admin.ModelAdmin):
    list_display = ("name", "state", "active")
    list_filter = ("active", "state__country")
    list_editable = ("active",)
    search_fields = ("name", "state__name", "state__country__name")

@admin.register(CourseCategoryMaster)
class CourseCategoryMasterAdmin(admin.ModelAdmin):
    list_display = ("name", "active")
    list_editable = ("active",)
    search_fields = ("name",)

# CollegeCategory and Course are master lists too, with full CRUD in Django Admin.
try:
    admin.site.register(CollegeCategory)
except admin.sites.AlreadyRegistered:
    pass

# Separate rich-information pages for Colleges and Courses.
from .models import CollegeAdditionalInformation, CollegeAdditionalGallery, CourseAdditionalInformation, CourseAdditionalGallery

class CollegeAdditionalGalleryInline(admin.TabularInline):
    model = CollegeAdditionalGallery
    extra = 1

@admin.register(CollegeAdditionalInformation)
class CollegeAdditionalInformationAdmin(admin.ModelAdmin):
    list_display = ("college", "has_campus_tour", "active")
    list_filter = ("active", "college__college_type", "college__state", "college__university")
    search_fields = ("college__name", "overview", "placement")
    autocomplete_fields = ("college",)
    inlines = [CollegeAdditionalGalleryInline]
    fieldsets = (
        ("College", {"fields": ("college", "active")}),
        ("Additional Text", {"fields": ("overview",)}),
        ("Campus Tours", {"fields": ("campus_tour_url",)}),
        ("Placement", {"fields": ("placement",)}),
    )
    @admin.display(boolean=True, description="Campus Tours")
    def has_campus_tour(self, obj): return bool(obj.campus_tour_url)

class CourseAdditionalGalleryInline(admin.TabularInline):
    model = CourseAdditionalGallery
    extra = 1

@admin.register(CourseAdditionalInformation)
class CourseAdditionalInformationAdmin(admin.ModelAdmin):
    list_display = ("course", "has_campus_tour", "active")
    list_filter = ("active", "course__category", "course__level")
    search_fields = ("course__name", "overview", "placement")
    autocomplete_fields = ("course",)
    inlines = [CourseAdditionalGalleryInline]
    fieldsets = (
        ("Course", {"fields": ("course", "active")}),
        ("Additional Text", {"fields": ("overview",)}),
        ("Campus Tours", {"fields": ("campus_tour_url",)}),
        ("Placement", {"fields": ("placement",)}),
    )
    @admin.display(boolean=True, description="Campus Tours")
    def has_campus_tour(self, obj): return bool(obj.campus_tour_url)
