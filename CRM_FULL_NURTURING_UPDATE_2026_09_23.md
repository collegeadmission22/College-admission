# CRM + Home hierarchy update — 23 Sep 2026

## Home page order
1. Course cards first.
2. Course cards show **College Category** highlighters.
3. Dedicated **College Categories** highlighted selector appears immediately below Courses.
4. College cards appear below the College Categories selector.
5. Distance / Online Education appears below Colleges.

## Lead CRM
- All public lead forms continue to upsert into Lead CRM by mobile number.
- Added Lead Category: Hot, Warm, Cold, Fresh, Follow-up, Admission Ready, Converted, Lost.
- Lead Source, pipeline status, call outcome, next action, assigned caller, follow-ups and complete remarks/activity history remain connected.
- Added per-user `can_add_own_leads` permission and **Add My Lead** page. User-created leads are assigned to and uploaded by that user.
- Existing scoped permissions ensure counsellors/agents/consultants see assigned or self-uploaded leads; admins/staff see broader CRM data.
- Bulk import/export, duplicate checking, templates and error reports remain available.
- Admin reports retain source, conversion, counsellor, course, college, city, follow-up and communication analysis.
- Communication templates support Email, WhatsApp, SMS and now RCS as a channel choice.
- Existing Day 1/3/7/15/30 nurture workflow and follow-up reminder commands remain available.

## Deployment
Run `python manage.py migrate` after updating because migration `0031_lead_category_rcs_user_own_leads.py` is included.
Provider credentials/API endpoints are still required for real Email/WhatsApp/SMS/RCS delivery.
