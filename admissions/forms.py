from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import BulkDataBatch, CRMApiKey, College, Course, Communication, ContactMessage, FollowUp, Lead, LeadRemark, StudentApplication, StudentDocument, UserProfile

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ["name", "father_name", "phone", "email", "course", "preferred_college"]
        labels = {
            "name": "Student Name",
            "father_name": "Father Name",
            "phone": "Mobile Number",
            "email": "Email",
            "city": "City",
            "course": "Course",
            "preferred_college": "College",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Student name"}),
            "father_name": forms.TextInput(attrs={"placeholder": "Father name"}),
            "phone": forms.TextInput(attrs={"placeholder": "10-digit mobile number", "inputmode": "numeric"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email address"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].required = True
        self.fields["phone"].required = True
        for optional in ["father_name", "email", "course", "preferred_college"]:
            self.fields[optional].required = False
        self.fields["course"].queryset = Course.objects.all().order_by("name")
        self.fields["preferred_college"].queryset = College.objects.filter(active=True).order_by("name")
        self.fields["course"].empty_label = "Select Course"
        self.fields["preferred_college"].empty_label = "Select College"

    def clean_phone(self):
        phone = "".join(c for c in self.cleaned_data["phone"] if c.isdigit())
        if len(phone) < 10:
            raise forms.ValidationError("Enter a valid 10-digit mobile number.")
        return phone[-10:]

    def validate_unique(self):
        # Existing mobile numbers update the existing CRM lead instead of duplicating it.
        return

    def save(self, commit=True):
        if not commit:
            return super().save(commit=False)
        values = self.cleaned_data
        existing = Lead.objects.filter(phone=values["phone"]).first()
        if existing:
            for field in ["name", "father_name", "email", "course", "preferred_college"]:
                value = values.get(field)
                if value not in (None, ""):
                    setattr(existing, field, value)
            existing.source = "Website"
            existing.save()
            return existing
        lead = super().save(commit=False)
        lead.source = "Website"
        lead.save()
        return lead

class LeadUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ["status", "call_outcome", "next_action", "assigned_to", "source", "course", "preferred_college"]

class FollowUpCompleteForm(forms.Form):
    outcome = forms.CharField(widget=forms.Textarea(attrs={"rows":3}), help_text="Record call result, parent response and agreed next action.")

class LeadRemarkForm(forms.ModelForm):
    class Meta:
        model = LeadRemark
        fields = ["remark"]
        widgets = {"remark":forms.Textarea(attrs={"rows":3, "placeholder":"Add counselling, parent or admission remark…"})}

class LeadImportForm(forms.Form):
    file = forms.FileField(help_text="Upload .xlsx or .csv. Mobile Number is required and used for deduplication.")
    assigned_to = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True), required=False)
    source = forms.ChoiceField(choices=Lead.SOURCE, initial="Other")
    def clean_file(self):
        item = self.cleaned_data["file"]
        if not item.name.lower().endswith((".xlsx", ".csv")):
            raise forms.ValidationError("Upload an Excel (.xlsx) or CSV (.csv) file.")
        if item.size > 10 * 1024 * 1024:
            raise forms.ValidationError("Maximum file size is 10 MB.")
        return item

class BulkDataImportForm(forms.Form):
    dataset = forms.ChoiceField(choices=BulkDataBatch.DATASETS)
    mode = forms.ChoiceField(choices=BulkDataBatch.MODES, initial="upsert")
    file = forms.FileField(help_text="Excel (.xlsx) or CSV, maximum 10 MB")
    image_zip = forms.FileField(required=False, label="Images ZIP (optional)", help_text="JPG, JPEG, PNG or WEBP files named exactly as listed in the spreadsheet; maximum 100 MB")
    def clean_file(self):
        item = self.cleaned_data["file"]
        if not item.name.lower().endswith((".xlsx", ".csv")):
            raise forms.ValidationError("Upload an Excel (.xlsx) or CSV (.csv) file.")
        if item.size > 10 * 1024 * 1024:
            raise forms.ValidationError("Maximum file size is 10 MB.")
        return item
    def clean_image_zip(self):
        item = self.cleaned_data.get("image_zip")
        if not item: return item
        if not item.name.lower().endswith(".zip"):
            raise forms.ValidationError("Images must be uploaded as one .zip file.")
        if item.size > 100 * 1024 * 1024:
            raise forms.ValidationError("Images ZIP cannot exceed 100 MB.")
        return item
    def clean(self):
        cleaned = super().clean()
        if cleaned.get("dataset") == "leads" and cleaned.get("image_zip"):
            self.add_error("image_zip", "Lead records do not have an image field. Upload images only for catalogue datasets.")
        return cleaned

class CommunicationForm(forms.ModelForm):
    class Meta:
        model = Communication
        fields = ["channel", "subject", "message"]
        widgets = {"message": forms.Textarea(attrs={"rows": 6, "placeholder": "Write or paste an approved message template…"})}

class FollowUpForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        fields = ["due_at", "note", "reminder_minutes_before", "notify_assignee_email", "notify_lead_whatsapp", "notify_lead_sms"]
        widgets = {"due_at": forms.DateTimeInput(attrs={"type": "datetime-local"})}

class ConsultantCreateForm(UserCreationForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20)
    organisation = forms.CharField(max_length=140, required=False)
    can_import_leads = forms.BooleanField(required=False, initial=True)
    can_export_leads = forms.BooleanField(required=False)
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "phone", "organisation", "can_import_leads", "can_export_leads", "password1", "password2"]
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name, user.last_name, user.email = self.cleaned_data["first_name"], self.cleaned_data["last_name"], self.cleaned_data["email"]
        if commit:
            user.save()
            UserProfile.objects.create(user=user, role="Consultant", phone=self.cleaned_data["phone"], organisation=self.cleaned_data["organisation"], can_import_leads=self.cleaned_data["can_import_leads"], can_export_leads=self.cleaned_data["can_export_leads"], active=True)
        return user

class ApiKeyCreateForm(forms.Form):
    name = forms.CharField(max_length=100, help_text="Example: Website lead connector")
    owner = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True))
    expires_at = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={"type":"datetime-local"}))

class StudentSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class StudentApplicationForm(forms.ModelForm):
    class Meta:
        model = StudentApplication
        exclude = ["user", "status", "submitted_at"]
        widgets = {"date_of_birth": forms.DateInput(attrs={"type": "date"}), "address": forms.Textarea(attrs={"rows": 3})}

class StudentDocumentForm(forms.ModelForm):
    class Meta:
        model = StudentDocument
        fields = ["document_type", "file"]
    def clean_file(self):
        file = self.cleaned_data["file"]
        extension = file.name.rsplit(".", 1)[-1].lower() if "." in file.name else ""
        if extension not in {"pdf", "jpg", "jpeg", "png"}:
            raise forms.ValidationError("Only PDF, JPG and PNG files are allowed.")
        if file.size > 5 * 1024 * 1024:
            raise forms.ValidationError("File size must be 5 MB or less.")
        return file

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "phone", "email", "subject", "message"]
        widgets = {"message": forms.Textarea(attrs={"rows": 5})}
