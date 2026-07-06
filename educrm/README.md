# EduVoice

A multi-tenant school feedback and CRM platform. Students reflect on their learning each term, teachers receive anonymous aggregated feedback, parents track their child's engagement, and school admins get a CRM analytics dashboard, all scoped per school for SaaS deployment.

Built curriculum-agnostic from the ground up: a school running Kenya's CBC, Cambridge IGCSE, the British National Curriculum, IB, or 8-4-4 all run on the same platform without code changes. The seed data demonstrates this directly by provisioning one CBC school and one Cambridge school side by side.

---

## What it does

**Students**
- End-of-term review for each subject and teacher, five dimensions, fully anonymous to teachers
- Values and skills self-rating: reading for pleasure, asking why, public speaking, adult interaction, teamwork, environmental care
- Positively framed reflection ("what did you love?", "what made you curious?") rather than a complaint form

**Teachers**
- Aggregated anonymous feedback per subject and class, no individual student identity ever surfaced
- Open-text student comments collected thematically
- Self-assessment form: syllabus coverage, student engagement, values integration, next-term goals

**Parents**
- Per-child report showing subject ratings and soft-skill self-ratings
- Visibility into the child's open-text reflections
- Ability to leave an encouraging note for the child

**School admins**
- School-wide participation rates and review counts
- Subject enjoyment rankings across classes
- Soft-skill averages across the school
- Teacher clarity ratings, visible only to admin, never to other teachers
- Semester management with a review-period open/close toggle

---

## Architecture

**Curriculum model.** `CurriculumFramework` (e.g. "CBC", "Cambridge International") and `CurriculumLevel` (e.g. "Primary", "IGCSE") replace what was originally a hardcoded two-tier Kenya-only enum. `Subject` and `ClassRoom` both reference these instead of a fixed grade range, so `ClassRoom.grade_label` is free text ("Grade 5", "Year 10", "Form 4", "DP2") rather than a bounded integer. A school administrator defines their own framework and levels; nothing in the codebase assumes CBC specifically.

**Multi-tenancy.** Every model is scoped to a `School` foreign key. Onboarding a new school is a data operation, not a deploy.

**Anonymity.** Enforced at the view layer. Teacher-facing queries aggregate before they ever reach a template; no code path returns individual student identity alongside a review to a teacher. School admins retain individual-level visibility for safeguarding purposes.

---

## Tech stack

- **Backend:** Python 3.12, Django 6
- **Database:** PostgreSQL in production (via `dj-database-url` and `DATABASE_URL`), SQLite for local development
- **Frontend:** Server-rendered HTML and CSS, no JS framework
- **Auth:** Django's built-in auth with a custom `User` model (student, teacher, parent, admin roles) and full password-reset flow via email
- **Static files:** WhiteNoise
- **Deployment:** Docker, deployed on Render via `render.yaml` as a Blueprint (web service plus managed Postgres)

---

## Project structure

```
educrm/
├── core/               Django project settings, root URLs
├── accounts/           Custom User model, auth views, password reset
├── schools/            School, ClassRoom, Enrollment, TeacherAssignment, ParentStudentLink
├── curriculum/         CurriculumFramework, CurriculumLevel, Subject, SoftSkill
├── reviews/            Semester, Review, SoftSkillRating, TeacherSelfAssessment, ParentAcknowledgement
├── dashboard/          Role-routed dashboard views, admin CRM analytics
├── templates/          HTML templates (base layout, per-role pages, landing page)
├── seed.py             Demo data: two schools on two different curricula, users, classrooms
├── Dockerfile           Multi-stage build
├── docker-compose.yml   Local dev with hot reload
├── render.yaml          Render Blueprint: web service + managed Postgres
└── manage.py
```

---

## Local development

```bash
git clone https://github.com/Anubis-ix/EduVoice.git
cd EduVoice/educrm

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python seed.py
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000)

### Docker

```bash
cd educrm
docker compose up
```

The bind mount persists `db.sqlite3` on your host machine between container restarts; no separate volume is needed for it.

---

## Deploying to Render

1. Push this repo to GitHub.
2. In the Render dashboard: New → Blueprint, connect the repo, set the Blueprint path to `educrm/render.yaml`.
3. Apply. Render provisions both the web service and a managed Postgres database, and wires `DATABASE_URL` between them automatically.
4. After the first deploy, go to the web service's Environment tab and fill in `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` (a Gmail address and an [app password](https://myaccount.google.com/apppasswords), not your regular login password). These are marked `sync: false` in the Blueprint so they're never committed to the repo.

The free Postgres tier does not lose data on redeploy or restart. The free web service tier spins down after 15 minutes of inactivity (roughly 30 seconds of cold start on the next request), but the database is unaffected by that.

---

## Demo credentials

Seeded by `seed.py`, two schools on two different curricula:

| School | Role | Username | Password |
|---|---|---|---|
| — | Superadmin | `superadmin` | `Admin1234!` |
| Nairobi Academy (CBC) | School admin | `admin.nairobi` | `Pass1234!` |
| Nairobi Academy (CBC) | Teacher | `ms.wanjiku` | `Pass1234!` |
| Nairobi Academy (CBC) | Student, Grade 5A | `jane.mwangi` | `Pass1234!` |
| Nairobi Academy (CBC) | Student, Grade 7B | `amina.hassan` | `Pass1234!` |
| Nairobi Academy (CBC) | Parent | `parent.mwangi` | `Pass1234!` |
| Brookhouse (Cambridge) | School admin | `admin.brookhouse` | `Pass1234!` |
| Brookhouse (Cambridge) | Teacher | `mr.smith` | `Pass1234!` |
| Brookhouse (Cambridge) | Student, Year 10 | `leila.khan` | `Pass1234!` |

---

## Roadmap

- Rewrite remaining landing-page copy that still reads Kenya/CBC-specific (hero badge, dedicated CBC section, footer tagline) now that the underlying platform is curriculum-agnostic
- School admin UI for managing semesters and curriculum frameworks (currently via Django admin)
- PDF report export for parents
- Multi-language support
- Progressive Web App for the student mobile experience
- API endpoints for integration with existing school management systems

---

## License

MIT
