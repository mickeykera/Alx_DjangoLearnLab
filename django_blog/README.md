
# Django Blog – Authentication, Tagging, and Search

This project adds authentication, tagging, and search to the Django blog, including registration, login, logout, user profile editor, post tagging, and keyword/tag search.


## Features
- User registration (username, email, password)
- Login / Logout using Django auth views
- Authenticated profile view and edit (username, email, first name, last name)
- CSRF protection on all forms
- Tagging: Add tags to posts, view posts by tag
- Search: Search posts by title, content, or tags


## App Structure
- Forms: `blog/forms.py` (`RegistrationForm`, `ProfileForm`, `PostForm` with tags)
- Models: `blog/models.py` (`Post` with tags, `Comment`)
- Views: `blog/views.py` (authentication, post CRUD, tagging, search)
- URLs: `blog/urls.py` (`/login`, `/logout`, `/register`, `/profile`, `/tags/<tag_name>/`, `/search/`)
- Templates:
   - `blog/templates/registration/login.html`
   - `blog/templates/registration/logout.html`
   - `blog/templates/registration/register.html`
   - `blog/templates/registration/profile.html`
   - `blog/templates/blog/post_list.html` (shows tags, search bar)
   - `blog/templates/blog/post_detail.html` (shows tags)
   - `blog/templates/blog/search_results.html` (search results)

## Settings
In `django_blog/settings.py`:
- `LOGIN_REDIRECT_URL = "profile"`
- `LOGOUT_REDIRECT_URL = "login"`
- Templates and static are already configured for app templates/static.

If using SQLite (default), no DB changes are required. For PostgreSQL, change `DATABASES['default']` accordingly and install `psycopg[binary]`.

## Usage
1. Create and apply migrations:
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
   - Posts by tag: `http://127.0.0.1:8000/tags/<tag_name>/`
   - Search: `http://127.0.0.1:8000/search/?q=keyword`


## Tagging and Search
- Add tags to posts when creating or editing. Enter tags separated by commas.
- Tags are shown on post list and detail pages. Click a tag to view all posts with that tag.
- Use the search bar on the posts list page to find posts by title, content, or tag.
- Search results show matching posts and their tags.


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
- Tagging uses [django-taggit](https://django-taggit.readthedocs.io/).
