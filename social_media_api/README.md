# Social Media API (minimal auth setup)

This project is a minimal Django + Django REST Framework project with a custom User model and token authentication.

Features added in this step:

- Custom `User` model extending Django's `AbstractUser` with fields: `bio`, `profile_picture`, and `followers` (ManyToMany to self).
- Django REST Framework + TokenAuthentication configured.
- Endpoints for registration, login (both return an auth token), and profile retrieval/update.

API endpoints (development):

- POST /api/accounts/register/ - create a new user. Request body: `username`, `email`, `password`, `first_name` (optional), `last_name` (optional), `bio` (optional). Returns user data with `token`.
- POST /api/accounts/login/ - login with `username` and `password`. Returns user data with `token`.
- GET /api/accounts/profile/ - retrieve current user's profile (requires token header `Authorization: Token <token>`).
- PUT/PATCH /api/accounts/profile/ - update current user's profile (requires token).

Setup (Windows PowerShell):

1. Create a virtual environment and install requirements (Django and djangorestframework):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -U pip
pip install django djangorestframework djangorestframework-authtoken pillow
```

2. Run migrations to create database and token model:

```powershell
python manage.py makemigrations
python manage.py migrate
```

3. Create a superuser (optional):

```powershell
python manage.py createsuperuser
```

4. Run the development server:

```powershell
python manage.py runserver
```

Testing with Postman / HTTP client:

- Register: POST JSON to `http://127.0.0.1:8000/api/accounts/register/` and note the returned `token`.
- Login: POST JSON to `http://127.0.0.1:8000/api/accounts/login/` and note the returned `token`.
- Use `Authorization: Token <token>` header for authenticated requests (profile endpoints).

Notes:
- `MEDIA_ROOT` is set to `./media` and `MEDIA_URL` to `/media/` for profile pictures. Uploading files requires a multipart/form-data request.
- During development `DEBUG=True`, so `MEDIA` files are served automatically via Django.

If you want, I can run migrations and start the server in this workspace now. Let me know and I'll proceed.
