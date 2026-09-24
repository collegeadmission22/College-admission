# Unified Lead Form Render Fix

- Added a global `apply_form` through the portal context processor so the modal has real Django form fields on every public page.
- Home and Contact override `apply_form` with their bound form so validation is preserved.
- Updated `_lead_form_fields.html` to consistently render `apply_form`.
- This fixes missing Student Name, Father Name, Mobile, Email, Course and College controls in the modal and keeps all channels connected to `quick_apply` / Lead CRM.
