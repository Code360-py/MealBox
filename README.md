# MealBox v1.0

A lightweight recipe browser built on top of TheMealDB. Django + Bootstrap 5 with a dark neon UI.

Live: https://xenonstudio.pythonanywhere.com

## Overview

MealBox is a recipe discovery web app. It fetches recipes, categories, images, and instructions from the public TheMealDB API and presents them in a mobile-first, iPhone-style interface. Users can browse, search, bookmark recipes, and manage their own account.

The project uses a custom session-based authentication layer. Django's built-in auth and admin apps are intentionally disabled.

## Features

### Recipe Discovery

- Browse recipes by category (Beef, Chicken, Seafood, Dessert, Vegetarian, and more)
- Full-text search by dish name
- Recent search history saved in localStorage (per browser)
- Recipe detail page with ingredients list, step-by-step instructions, YouTube link, and share row

### Bookmarks

- Save any recipe to a personal collection
- Remove bookmarks from either the recipe page or the bookmarks list
- Bookmark count and recent saves shown on the account page

### Seasonal Collections

- Christmas: holiday recipes, auto-surfaces from Dec 1 to Jan 6
- Diwali: Indian festive dishes, auto-surfaces from Oct 15 to Nov 15
- Birthday: cakes and celebration desserts, always available
- The sidebar shows a live hint of the next upcoming festival

### Accounts

- Custom session-based auth (no Django auth app)
- Register with username, email, optional date of birth
- Login, logout, permanent account deletion
- Optional date of birth with automatic birthday greeting on the day
- Personal profile page with stats and activity

### UI and UX

- Dark neon theme: cyan (#00e5ff) and purple (#a855f7) accents
- Fixed iOS-style top notch bar with hamburger menu
- Slide-in sidebar with grouped navigation
- Fixed bottom tab bar (Home, Search, Saved, Account)
- YouTube-style skeleton preloading on images
- Top progress bar on page navigation
- Full-screen overlay spinner on form submit
- Image blur-up fade-in
- Respects prefers-reduced-motion
- Mobile-first, with desktop fallback at 900px max content width

## Tech Stack

- Backend: Django 6.1.1
- Database: SQLite
- HTTP client: requests
- Static files: Whitenoise
- Frontend: Bootstrap 5.3.8
- Icons: Font Awesome 7.0.1
- Fonts: Noto Sans (Google Fonts)
- API: TheMealDB (https://www.themealdb.com/api.php)

## Project Structure

    MealBox/
    |-- MealBox/
    |   |-- __init__.py
    |   |-- settings.py
    |   |-- urls.py
    |   |-- asgi.py
    |   `-- wsgi.py
    |-- Meal/
    |   |-- migrations/
    |   |-- static/
    |   |   |-- css/style.css
    |   |   `-- js/
    |   |       |-- app.js
    |   |       `-- search-history.js
    |   |-- templates/
    |   |   |-- include/
    |   |   |   |-- base.html
    |   |   |   |-- topbar.html
    |   |   |   |-- sidebar.html
    |   |   |   |-- bottomtabs.html
    |   |   |   `-- footer.html
    |   |   |-- Content/
    |   |   |   |-- account.html
    |   |   |   |-- about.html
    |   |   |   |-- contact.html
    |   |   |   |-- login.html
    |   |   |   |-- register.html
    |   |   |   |-- bookmarks.html
    |   |   |   |-- christmas.html
    |   |   |   |-- diwali.html
    |   |   |   |-- birthday.html
    |   |   |   `-- delete_account.html
    |   |   |-- index.html
    |   |   |-- search.html
    |   |   |-- meals.html
    |   |   `-- meal_view.html
    |   |-- auth.py
    |   |-- models.py
    |   |-- urls.py
    |   |-- views.py
    |   |-- admin.py
    |   |-- apps.py
    |   `-- tests.py
    |-- db.sqlite3
    |-- manage.py
    |-- requirements.txt
    |-- .gitignore
    `-- README.md

## Local Development

1. Clone the repository

    git clone https://github.com/your-username/mealbox.git
    cd mealbox

2. Create a virtual environment

    python -m venv venv

Activate it.

Linux or macOS:

    source venv/bin/activate

Windows:

    venv\Scripts\activate

3. Install dependencies

    pip install -r requirements.txt

4. Apply migrations

    python manage.py makemigrations
    python manage.py migrate

5. Run the development server

    python manage.py runserver

Open http://127.0.0.1:8000/ in your browser.

## Environment Variables

In production the app reads DJANGO_SECRET_KEY from the environment. If unset, it falls back to a development key.

Set it in your shell before running in production:

    export DJANGO_SECRET_KEY="your-long-random-secret-key-here"

Generate a secure key with:

    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

## Routes

- / : home : Home page with categories grid and seasonal banners
- /search/ : search : Search page with recent-search history
- /about/ : about : About page
- /contact/ : contact : Contact form
- /christmas/ : christmas : Christmas recipe collection
- /diwali/ : diwali : Diwali recipe collection
- /birthday/ : birthday : Birthday recipe collection
- /login/ : login : Login
- /register/ : register : Register
- /logout/ : logout_view : Logout
- /account/ : account : Profile page
- /account/dob/ : save_dob : Update date of birth
- /account/delete/ : delete_account : Permanent account deletion
- /bookmarks/ : bookmark_list : Saved recipes
- /bookmark/toggle/ : toggle_bookmark : Add or remove a bookmark
- /meal/category/<category>/ : filterCalegory : Recipes in a category
- /meal/recipe/<meal_id>/ : mealDetails : Recipe detail page

## Data Models

### User

Custom user model with session-based authentication.

- username: CharField(150), unique
- email: EmailField, unique
- password_hash: CharField(128), salted SHA-256
- password_salt: CharField(32), random per user
- date_of_birth: DateField, nullable
- created_at: DateTimeField, auto
- is_active: BooleanField, default True

Methods: set_password, check_password, is_birthday_today, age.

### Bookmark

- user: ForeignKey(User), cascade delete
- meal_id: CharField(100), TheMealDB ID
- meal_name: CharField(255)
- meal_thumb: URLField, nullable
- created_at: DateTimeField, auto

Unique constraint: (user, meal_id).

## Authentication

This project does not use django.contrib.auth. Instead:

- Passwords are hashed with salted SHA-256 (Meal/models.py)
- Sessions store the user ID under request.session['user_id']
- Meal/auth.py provides:
  - login_user(request, user)
  - logout_user(request)
  - get_current_user(request)
  - login_required decorator

Note on hashing: Salted SHA-256 is used for simplicity. For production deployments handling sensitive data, swap to bcrypt or argon2 by replacing User._hash and the set_password / check_password implementations.

## Deployment on PythonAnywhere

### 1. Upload the code

From your local machine, zip the project (excluding the virtualenv and DB):

    zip -r MealBox.zip MealBox -x "*/__pycache__/*" "*/venv/*" "*/staticfiles/*" "*.sqlite3*"

Upload MealBox.zip via the Files tab on PythonAnywhere and extract:

    cd ~
    unzip MealBox.zip

Alternatively, push to GitHub and git clone from the PythonAnywhere console.

### 2. Create a virtualenv

    mkvirtualenv --python=/usr/bin/python3.10 mealbox-venv
    pip install -r ~/MealBox/requirements.txt

### 3. Migrate and collect static files

    cd ~/MealBox
    python manage.py migrate
    python manage.py collectstatic --noinput

### 4. Configure the Web app

Go to the Web tab and click Add a new web app, then Manual configuration, then Python 3.10.

Set:

- Source code: /home/xenonstudio/MealBox
- Working directory: /home/xenonstudio/MealBox
- Virtualenv: /home/xenonstudio/.virtualenvs/mealbox-venv

### 5. Edit the WSGI configuration file

Replace its contents with:

    import os
    import sys

    path = '/home/xenonstudio/MealBox'
    if path not in sys.path:
        sys.path.insert(0, path)

    os.environ['DJANGO_SETTINGS_MODULE'] = 'MealBox.settings'
    os.environ['DJANGO_SECRET_KEY'] = 'REPLACE-WITH-A-REAL-SECRET-KEY'

    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

### 6. Static files mapping

In the Static files section of the Web tab add:

- URL: /static/
- Directory: /home/xenonstudio/MealBox/staticfiles/

### 7. Reload

Click the green Reload button. Visit:

    https://xenonstudio.pythonanywhere.com

## Troubleshooting

- DisallowedHost: add the domain to ALLOWED_HOSTS in settings.py
- ModuleNotFoundError: whitenoise: pip install whitenoise inside the venv
- CSS or JS missing on live site: point /static/ at staticfiles/, not Meal/static/
- 500 error with no visible cause: temporarily set DEBUG=True in settings.py, reload, read the traceback, then revert
- no such table errors: run python manage.py migrate
- Skeleton images never fade in: hard refresh and check the browser console

Check the Error log link on the Web tab for PythonAnywhere-specific issues.

## Release Notes for v1.0

First public release.

- Full recipe browsing, search, and bookmark system
- Custom session-based authentication (no Django auth)
- Seasonal collections: Christmas, Diwali, Birthday
- Account management with optional date of birth and permanent deletion
- Dark neon iOS-style UI with skeleton preloading and progress bar
- Whitenoise static file serving
- Deployed on PythonAnywhere at https://xenonstudio.pythonanywhere.com

## License

Personal project by Xenon Studio.
