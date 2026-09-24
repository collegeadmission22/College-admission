# Modular CRM Upgrade
Added professional CRM Control Center and module workspaces for College, Course, Online Course, Student, Medical College, Social/SEO, Entrance Exam, Classroom, Employee/HR, Counsellor/Calling, Leads, Communications, Finance, Tasks, Reports, Partners, and Roles/Permissions.

## Role security
`ModuleAccess` provides per-user View/Add/Edit/Delete/Import/Export/Assign/Approve flags. Superusers and Admin/Super Admin roles bypass module restrictions.

## New operational models
EntranceExam, Classroom, SocialSEOItem, EmployeeRecord, CRMTask.

## First run after upgrade
```powershell
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py makemigrations admissions
python manage.py migrate
python manage.py runserver
```
Then open `/admin/` to assign Module Access records to users and `/crm/` for the Control Center.
