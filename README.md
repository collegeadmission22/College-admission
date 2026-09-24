# College Admission Portal (Python/Django)

A responsive admission website plus a built-in counsellor CRM and student application portal. It includes college/course image uploads, enquiry capture, About/Contact pages, staff authentication, lead stages, assignments, follow-ups, student registration, online applications, document uploads, admin verification tools, and PostgreSQL support.

## Run on Windows

1. Install Python 3.12 and open Command Prompt in this folder.
2. Create and activate an environment:
   `python -m venv venv`
   `venv\\Scripts\\activate`
3. Install and prepare:
   `pip install -r requirements.txt`
   `python manage.py makemigrations admissions`
   `python manage.py migrate`
   `python manage.py seed_data`
   `python manage.py createsuperuser`
4. Start: `python manage.py runserver`
5. Website: http://127.0.0.1:8000 — Admin: http://127.0.0.1:8000/admin

## Upload course and college pictures

Open `/admin/`, choose **Courses** or **Colleges**, edit a record and upload its image/logo. You can also enter an external licensed image URL and its source page; source credits are shown on catalogue cards. Never use a generic building photo as an actual campus photo. Student documents are stored under `media/student_documents/`; production hosting must use private object storage and authenticated downloads for sensitive files.

## PostgreSQL

All CRM records—including leads, assignments, follow-ups, communication logs, consultant roles, student applications and API-key hashes—are stored in PostgreSQL whenever `DATABASE_URL` is configured.

Copy `.env.example` to `.env`, replace the sample password, and set:
`DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/college_admission_db`

### Run PostgreSQL with Docker

1. Copy `.env.example` to `.env` and change `POSTGRES_PASSWORD` and `SECRET_KEY`.
2. Run `docker compose up --build -d`.
3. Open http://127.0.0.1:8000 and check http://127.0.0.1:8000/health/.
4. Create the first administrator with `docker compose exec web python manage.py createsuperuser`.

The named Docker volume `college_admission_postgres` keeps database data when containers restart or are rebuilt. Do not run `docker compose down -v` unless you intentionally want to delete the database volume.

### Backup and restore

Create a backup:

`docker compose exec -T postgres pg_dump -U college_admission_user -d college_admission_db -Fc > college_admission_backup.dump`

Restore into an empty/replacement database only after confirming the target:

`docker compose exec -T postgres pg_restore -U college_admission_user -d college_admission_db --clean --if-exists < college_admission_backup.dump`

Schedule encrypted off-server backups for production and regularly test restoration. Database backups do not include uploaded media files; back up private document storage separately.

For production set `DEBUG=False`, `DB_SSL_REQUIRED=True`, use a strong `SECRET_KEY`, add your domain to `ALLOWED_HOSTS`, run `python manage.py collectstatic --noinput`, and serve with `gunicorn config.wsgi:application`.

## Deploy on Render

1. Upload this project to a GitHub repository.
2. In Render, select **New > Blueprint** and connect the repository.
3. Render reads `render.yaml`, creates the web service and PostgreSQL database, runs migrations, and loads starter content.
4. When deployment finishes, open the generated `onrender.com` URL.
5. Open the Render Shell and run `python manage.py createsuperuser` for the first admin account.

The included free configuration is suitable for a live demonstration. Free services use temporary local storage, so uploaded images and student documents can disappear after a restart or redeploy. Before accepting real student documents, configure private cloud object storage or upgrade to a persistent disk, use a custom domain, and enable backups.

## Social channels, WhatsApp and chatbot

Open `/admin/` and edit **Social links** to add the official Instagram, YouTube and LinkedIn page URLs. Facebook is preloaded with the College Admission page. Social clicks are recorded for reporting. Set `WHATSAPP_NUMBER` as an international-format number without `+` or spaces. The website admission chatbot stores questions in **Chat messages** and answers common course, college, fee, scholarship, application and document questions. A generative AI provider can be connected later through a server-side API key.

## Catalogue pages and Apply popup

- `/courses/` shows the visual course catalogue with motivational and career descriptions.
- `/colleges/` filters IPU, MDU, AKTU, KUK and Other colleges by university group and state.
- `/medical-colleges/` shows the state-wise medical catalogue and NEET guidance calls to action.
- In `/admin/`, open **Site settings** to upload the header logo and switch the Apply popup or automatic opening on/off.
- Every catalogue image/card has an Apply call to action. Add more colleges and states in Admin as the database grows.

## Role-based CRM and bulk leads

- Create a Django user, then add its **User profile** in Admin with one role: Admin, Staff, Employee, Agent, Consultant or College.
- Admin/Staff can see all leads. Employees, Agents and Consultants see leads assigned to or uploaded by them. College users see leads for their linked college.
- Consultants and authorised users can open `/crm/import/` to upload `.xlsx` or `.csv` files and assign the rows to a caller.
- Required import headings are `Student Name` and `Mobile Number`; optional headings are `Email`, `City`, `Course` and `JEE / CLAT`.
- Mobile number is unique. A repeated mobile updates the existing lead rather than creating a duplicate.
- Excel and CSV exports follow the logged-in user's role and visibility permissions.
- From a lead page, staff can save email, WhatsApp and SMS drafts or send through configured SMTP/API credentials. Every attempt is recorded in Communication History.

## Bulk Data Management

- Admin, Super Admin, Admission Manager and Staff users can open `/crm/bulk-data/` from the **Bulk Upload Data** dashboard button.
- Excel (`.xlsx`) and CSV import/export is available for Leads, Courses, Colleges, Medical Colleges and Online Courses.
- Download the dataset template before importing. Choose **Create new only** to skip existing matches or **Create and update** to update them.
- Matching keys are: unique mobile for Leads, name for Courses, name + university for Colleges, name + state for Medical Colleges, and title for Online Courses.
- Every import records uploader, filename, mode, row totals, created/updated/skipped/rejected totals and a downloadable CSV error report.
- Catalogue templates include **Image Filename** and college templates also include **Logo Filename**. Upload the matching JPG/JPEG/PNG/WEBP files together in the optional Images ZIP (maximum 100 MB; each image maximum 5 MB). External licensed image/source URLs remain supported.
- Leads are data-only because the lead record has no image field. Course, College, Medical College and Online Course images can be uploaded in bulk.
- Run `python manage.py migrate` after upgrading an existing installation so migrations `0010` and `0011` create and extend the audit table.

## Follow-up calendar and automatic reminders

- `/crm/calendar/` shows role-scoped follow-ups by date and time.
- While scheduling a follow-up, select email to notify the assigned employee/agent and optionally WhatsApp or SMS to notify the lead.
- Run `python manage.py send_followup_reminders` every few minutes. The included Render cron service runs it every 10 minutes.
- SMTP, WhatsApp and SMS credentials must be configured as environment variables for both the web service and reminder cron service. A failed provider call is recorded and does not expose credentials.
- The lead page now follows the complete journey: New Enquiry, First Call, Contacted/Interested, Hot/Warm/Cold, Visit/Counselling, Documents, Application, Offer/Fee and Admission Confirmed. Each stage change, call outcome, assignment, follow-up and message is written to the activity history.
- Complete each follow-up with its call result and agreed next action; completed tasks remain visible for audit.

## SMTP, WhatsApp and SMS credentials

- CRM Admins can open `/crm/integrations/` to see whether each service is configured and safely test SMTP. Tokens and passwords are never shown.
- Local development reads credentials from `.env`; production credentials belong in the hosting provider's secret environment settings.
- WhatsApp requires a Meta WhatsApp Business Cloud API Phone Number ID endpoint and access token. Messages outside the customer-service window must use Meta-approved templates.
- Indian SMS sending requires your provider API endpoint/auth key plus DLT-approved sender ID and templates.
- `.env`, `.env.*`, private keys and common credential files are excluded through `.gitignore`; `.env.example` remains available as the safe blank template.
- After adding or changing any credential, stop and restart the local Django server. On Render, save the environment variables and redeploy both the web service and reminder cron service.

## Admin-authorised consultants and CRM API

- `/crm/consultants/` lets only a superuser or CRM Admin create an authorised Consultant login and choose import/export permissions.
- `/crm/api-keys/` lets only a superuser or CRM Admin generate, expire and revoke API keys. The full secret is displayed once; only a SHA-256 hash is stored.
- Send website or partner leads to `POST /api/v1/leads/` with the key in the `X-API-Key` header. JSON requires `name` and `mobile`; supported optional fields are `email`, `city`, `course`, `score`, `source` and `consent`.
- API lead intake uses the same unique mobile rule: an existing mobile is updated instead of duplicated.

## Recommended next integrations

Connect WhatsApp Business Cloud API, email, SMS/RCS, Meta lead ads and YouTube through background tasks and webhooks. Credentials must be environment variables, never stored in source code.

## Complete CRM modules

- Lead profiles now include father name, unique mobile, email, city, course/college, Class 10/12 percentages, entrance rank, source, counsellor, call outcome, next action and permanent remarks.
- Roles include Super Admin, Admin, Admission Manager, Counsellor, Data Entry Operator, Staff, Employee, Agent, Consultant and College. CRM visibility remains scoped by role and assignment.
- `python manage.py run_lead_nurturing` processes consent-based Day 1, 3, 7, 15 and 30 communication steps and schedules the first counsellor call. Render includes a daily nurturing cron service.
- `/crm/reports/` shows headline admissions, pending follow-ups, source/course totals and counsellor performance. Export routes support Excel, CSV and PDF plus today/hot/admission filters.
- Student dashboards show application, documents, fee status and notifications. Resume and certificate uploads are supported.
- Login supports Remember Me. Passwords require at least eight characters with uppercase, lowercase, number and special character. Django's secure email reset-link flow is available from Forgot Password.
