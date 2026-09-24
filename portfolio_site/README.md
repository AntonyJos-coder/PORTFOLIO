# Antony Jos — Portfolio Website (Django)

A single-page, recruiter-focused portfolio for a Computer Engineering
graduate, built in Django. The database already contains Antony Jos's
verified information (education, skills, internships/training, and the
site itself as a project) — no placeholder/sample content remains.
Everything is editable from the Django admin, no code changes required.

## Features
- Sticky header with smooth-scroll navigation and an active-section indicator
- Hero section that immediately states who you are, what you do, and what
  you're looking for, with Resume / Projects / Contact CTAs
- About Me section with a quick-facts panel (Open to, location, currently exploring)

- Skills grouped by category (Programming, Web, Backend, Database,
  Application Development) as clean chips — no invented skills or
  exaggerated levels
- Education & Experience/Internship timelines
- A Featured Project section plus a projects grid, each with tech badges
  and Source/Live Demo buttons
- Contact form that saves messages to the database, with visible
  success/error states (view submissions in the admin)
- Subtle fade-up/hover animations that respect `prefers-reduced-motion`
- Fully responsive (tested 320px–1920px), keyboard-accessible, WCAG-minded
  contrast
- Resume, GitHub and LinkedIn buttons automatically show a clearly
  disabled/"add link" state instead of a fake or dead link when those
  fields are empty in the admin

## Setup

```bash
python3 -m venv venv
source venv/bin/activate        # venv\Scripts\activate on Windows
pip install -r requirements.txt

python manage.py migrate
python manage.py seed_profile   # (re)loads Antony's verified profile/education/skills/experience/projects
python manage.py createsuperuser
python manage.py runserver
```

Visit **http://127.0.0.1:8000/** for the site and
**http://127.0.0.1:8000/admin/** to edit your content.

> The shipped `db.sqlite3` already has the real content loaded, so
> `seed_profile` is only needed if you reset the database.

## Editing your content
Log into `/admin` and fill in what's still missing:
1. **Profile** — add a profile photo (optional — falls back to an "AJ"
   identity card), a resume PDF, your email, and GitHub/LinkedIn URLs.
   Edit **Open to**, **Open to note**, and **Currently exploring**
   (`learning_focus`, comma-separated) from the About sidebar group.
   Everything else (name, title, About Me) is already set.
2. **Education** — already has your Diploma from Carmel Polytechnic
   College. Add more entries if needed.
3. **Skills** — already has your confirmed stack, grouped by category.
   Add or remove skills and pick a category for each.
4. **Experience** — has your BSNL and Verdant entries. Add a description
   of what you did/learned at each (currently blank, marked as
   "Details to be added" on the site).
5. **Projects** — has one real project (this website itself). Add your
   other projects here — title, summary, tech stack (comma-separated),
   an image, and optional live-demo/source links. Tick "featured" to
   feature one in the Featured Project section.
6. **Contact messages** — read messages people send you through the site.

## Project layout
```
portfolio_site/        Django project settings/urls
portfolio/              App: models, views, forms, admin, migrations
  templates/portfolio/  base.html, home.html
static/css/style.css    Site styling (design tokens at the top)
static/js/main.js       Sticky header, mobile nav, scroll-spy, scroll reveal
```

## Before deploying
- Set `DEBUG=False` and a real `SECRET_KEY` in environment variables
- Set `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` to your domain
- Set `DATABASE_URL` to Postgres (required on Vercel)
- Run `python manage.py migrate` against that database
- Run `python manage.py collectstatic`

## Deploy on Vercel
1. Import this repository. Set **Root Directory** to `portfolio_site` *or* deploy from the repo root (both `vercel.json` files are included).
2. Add environment variables: `SECRET_KEY`, `DATABASE_URL`, `DEBUG=False`, plus `ALLOWED_HOSTS` / `CSRF_TRUSTED_ORIGINS` if you use a custom domain.
3. Run `python manage.py migrate` and `python manage.py createsuperuser` against the same Postgres URL (local machine or a one-off job). Vercel’s filesystem is ephemeral, so SQLite and uploaded media will not persist — keep images/resume in static files or object storage.
4. Deploy. Static files are served by WhiteNoise.
