# Django Blog – Authentication

This project adds a basic authentication system to the Django blog, including registration, login, logout, and a simple user profile editor.

## Features
- User registration (username, email, password)
- Login / Logout using Django auth views
- Authenticated profile view and edit (username, email, first name, last name)
- CSRF protection on all forms

## App Structure
- Forms: `blog/forms.py` (`RegistrationForm`, `ProfileForm`)
- Views: `blog/views.py` (`register`, `profile`, `home`)
- URLs: `blog/urls.py` (`/login`, `/logout`, `/register`, `/profile`)
- Templates:
  - `blog/templates/registration/login.html`
  - `blog/templates/registration/logout.html`
  - `blog/templates/registration/register.html`
  - `blog/templates/registration/profile.html`
  - Base blog page: `blog/templates/blog/home.html`

## Settings
In `django_blog/settings.py`:
- `LOGIN_REDIRECT_URL = "profile"`
- `LOGOUT_REDIRECT_URL = "login"`
- Templates and static are already configured for app templates/static.

If using SQLite (default), no DB changes are required. For PostgreSQL, change `DATABASES['default']` accordingly and install `psycopg[binary]`.

## Usage
1. Create and apply migrations (already done for `Post`):
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
2. Run the development server:
   ```bash
   python manage.py runserver
   ```
3. Open the site:
   - Home: `http://127.0.0.1:8000/`
   - Login: `http://127.0.0.1:8000/login/`
   - Register: `http://127.0.0.1:8000/register/`
   - Profile: `http://127.0.0.1:8000/profile/` (requires login)
   - Posts list: `http://127.0.0.1:8000/posts/`
   - New post: `http://127.0.0.1:8000/posts/new/` (requires login)

## Testing the Authentication Flow
- Register: Go to `/register/`, fill in username, email, and password. On success, you’re redirected to login.
- Login: Go to `/login/`, enter credentials. On success, you’re redirected to `/profile/`.
- Profile: View and edit your user fields. Submit to save changes. CSRF is enforced.
- Logout: Visit `/logout/`.

## Managing Posts (CRUD)
- Browse posts at `/posts/` and click a title for details.
- Create a post at `/posts/new/` (must be logged in).
- Edit your own post at `/posts/<id>/edit/`.
- Delete your own post at `/posts/<id>/delete/` (confirmation page).

Permissions:
- Anyone can view the list and detail pages.
- Only authenticated users can create posts.
- Only the author can edit or delete their posts.

## Comments
- Comments appear on the post detail page below the content.
- Add a comment on a post detail page (logged in): form posts to `/posts/<post_id>/comments/new/`.
- Edit your comment: `/comments/<id>/edit/`.
- Delete your comment: `/comments/<id>/delete/` (confirmation page).

Permissions:
- Anyone can read comments.
- Only authenticated users can add comments.
- Only the comment author can edit or delete their comment.

## Notes
- Static warning: If you see a warning about `STATICFILES_DIRS` path not existing, create the folder `django_blog/static/` or remove it from settings.
- Passwords are stored using Django’s built-in password hashing.
