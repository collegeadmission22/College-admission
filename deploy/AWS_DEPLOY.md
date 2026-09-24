# Repository baseline and AWS update path

This baseline was prepared from the 23 September CRM ZIP, **not from the Windows working directory or the running EC2 tree**. Compare it with both before making the first commit or restarting the live service. The repository currently has no commits. Use `main` as the deployment branch only after that comparison.

## Project layout

- `manage.py`, `config/`, `admissions/` (including migrations), `templates/`, `static/`: Django source.
- `requirements.txt`, `Dockerfile`, `docker-compose.yml`, `build.sh`, `render.yaml`: existing build options. AWS below uses a Python virtual environment, systemd, Nginx, and the existing RDS database; Docker/Render files are not the AWS deployment path.
- `deploy/college-admission.service.example`, `deploy/nginx.conf.example`: examples to adapt to the server. Never copy them over an existing live configuration blindly.
- `.env.example`: placeholders only. Keep `.env`, uploaded `media/`, `staticfiles/`, dumps and virtual environments outside Git.

## First import from Windows PowerShell

Use the **current working project** at `D:\Website\...`, after comparing it with this baseline. Change `$Project` to its actual directory. Make a separate copy or backup first.

```powershell
$Project = 'D:\Website\YOUR_CURRENT_PROJECT'
Set-Location $Project
# If .git already exists, inspect git remote -v and git log before proceeding.
git init
git branch -M main
git remote add origin https://github.com/collegeadmission22/College-admission.git
# Copy the reviewed .gitignore and .env.example from this baseline first.
git status --short --ignored
git add .gitignore .env.example manage.py config admissions templates static requirements.txt Dockerfile docker-compose.yml build.sh render.yaml README.md deploy
# Inspect exact staged names and any exposed values before committing.
git diff --cached --name-only
git diff --cached --check
git diff --cached
# Ensure .env, keys, virtual environment, media, staticfiles and dumps are absent.
git commit -m "Establish reviewed Django CRM baseline"
git push -u origin main
```

If `git remote add origin` reports an existing remote, inspect `git remote -v` and use `git remote set-url origin https://github.com/collegeadmission22/College-admission.git` only if it belongs to this project. If the repository gains a commit before your push, fetch and review it; do not force push.

## One-time AWS link (Ubuntu EC2)

Run in an SSH session on the server. Back up the existing code and database independently before replacing a live checkout. Confirm `/var/www/college_admission` and service name on this server. The commands below assume the service is `college-admission` and the repo can be cloned using a GitHub credential or read-only deploy key. Do not put credentials in the Git URL.

```bash
cd /var/www/college_admission
git status --short --branch
git remote -v
# Only if this directory is already a Git checkout for the same source:
git remote add origin https://github.com/collegeadmission22/College-admission.git
git fetch origin main
git diff --stat HEAD origin/main
git diff HEAD origin/main
```

If this is not a Git checkout, clone into **a new sibling directory**, install dependencies there, then switch the service `WorkingDirectory` and Gunicorn path during a planned cutover. Keep the existing `/var/www/college_admission` as a rollback copy. Preserve production `.env`, RDS settings and `media/` outside the checkout. The committed systemd and Nginx files are examples; adapt paths and private media handling before enabling them. Avoid `seed_data` on production unless you review its effects.

## Routine updates

Windows PowerShell, after reviewing changes:

```powershell
Set-Location 'D:\Website\YOUR_CURRENT_PROJECT'
git status --short
git diff --check
git add -u
git add path\to\new_source_file.py
git diff --cached --name-only
git diff --cached
git commit -m "Describe the CRM change"
git push origin main
```

On Ubuntu, after the repository and service are verified:

```bash
cd /var/www/college_admission
git status --short
git fetch origin main
git diff --stat HEAD origin/main
git diff HEAD origin/main
# Only if clean and the reviewed update should go live:
git merge --ff-only origin/main
/var/www/college_admission/venv/bin/python -m pip install -r requirements.txt
/var/www/college_admission/venv/bin/python manage.py check --deploy
/var/www/college_admission/venv/bin/python manage.py migrate --plan
/var/www/college_admission/venv/bin/python manage.py migrate
/var/www/college_admission/venv/bin/python manage.py collectstatic --noinput
sudo systemctl restart college-admission
sudo systemctl status college-admission --no-pager
curl -I https://collegeadmission.co.in/health/
```

For changes to dependencies or migrations, plan a rollback and database backup before applying them. `git` only moves code; existing RDS data and uploaded pictures require their own backup and storage plan. Never use `git reset --hard` on the live directory to resolve uncommitted changes.
