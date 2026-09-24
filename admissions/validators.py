import re
from django.core.exceptions import ValidationError

class StrongPasswordValidator:
    def validate(self, password, user=None):
        if not (re.search(r"[A-Z]", password) and re.search(r"[a-z]", password) and re.search(r"\d", password) and re.search(r"[^A-Za-z0-9]", password)):
            raise ValidationError("Password must include uppercase, lowercase, number and special character.")
    def get_help_text(self): return "Include at least one uppercase letter, lowercase letter, number and special character."
