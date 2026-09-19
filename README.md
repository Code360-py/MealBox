# MealBox v2.0

A lightweight recipe browser built on top of TheMealDB. Django + Bootstrap 5 with a dark neon UI.

Live: https://xenonstudio.pythonanywhere.com

## Overview

MealBox is a recipe discovery web app. It fetches recipes, categories, images, and instructions from the public TheMealDB API and presents them in a mobile-first, iPhone-style interface.

Django's built-in auth and admin apps are intentionally disabled. The project uses a custom session-based authentication layer instead.

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

## Tech Stack

- Backend: Django 6.1.1
- Database: SQLite
- HTTP client: requests
- Static files: Whitenoise
- Frontend: Bootstrap 5.3.8
- Icons: Font Awesome 7.0.1
- Fonts: Noto Sans (Google Fonts)
- API: TheMealDB (https://www.themealdb.com/api.php)

## Local Development

1. Clone the repository

    git clone https://github.com/Code360-py/MealBox.git
    cd MealBox

2. Create a virtual environment

    python -m venv venv
    source venv/bin/activate

3. Install dependencies

    pip install -r requirements.txt

4. Apply migrations

    python manage.py makemigrations
    python manage.py migrate

5. Run the development server

    python manage.py runserver

Open http://127.0.0.1:8000/

## Environment Variables

In production the app reads DJANGO_SECRET_KEY from the environment.

    export DJANGO_SECRET_KEY="your-long-random-secret-key-here"

Generate one with:

    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

## Routes

- / : home
- /search/ : search
- /about/ : about
- /contact/ : contact
- /christmas/ : christmas
- /diwali/ : diwali
- /birthday/ : birthday
- /login/ : login
- /register/ : register
- /logout/ : logout_view
- /account/ : account
- /account/dob/ : save_dob
- /account/delete/ : delete_account
- /bookmarks/ : bookmark_list
- /bookmark/toggle/ : toggle_bookmark
- /meal/category/<category>/ : filterCalegory
- /meal/recipe/<meal_id>/ : mealDetails

## Authentication

This project does not use django.contrib.auth. Instead:

- Passwords are hashed with salted SHA-256 (Meal/models.py)
- Sessions store the user ID under request.session['user_id']
- Meal/auth.py provides login_user, logout_user, get_current_user, and the login_required decorator

For production deployments handling sensitive data, swap to bcrypt or argon2 by replacing User._hash and the set_password / check_password implementations.

## Deployment on PythonAnywhere

See the full deployment section in this file's history or the project wiki.

Basic steps:

    mkvirtualenv --python=/usr/bin/python3.10 mealbox-venv
    pip install -r ~/MealBox/requirements.txt
    cd ~/MealBox
    python manage.py migrate
    python manage.py collectstatic --noinput

Then set up a Web app in the PythonAnywhere dashboard:

- Source code: /home/xenonstudio/MealBox
- Working directory: /home/xenonstudio/MealBox
- Virtualenv: /home/xenonstudio/.virtualenvs/mealbox-venv
- Static files: /static/ -> /home/xenonstudio/MealBox/staticfiles/

## Release Notes for v2.0

Full visual and architectural rewrite of the V1 recipe browser.

- Dark neon iOS-style UI
- Custom session-based authentication layer (no Django auth)
- Removed Django admin
- Dedicated search page with localStorage history
- Seasonal collections: Christmas, Diwali, Birthday
- Account page with profile, stats, and permanent delete
- Optional date of birth with automatic birthday greeting
- Bottom tab bar navigation
- Sidebar with grouped sections and next-festival hint
- YouTube-style skeleton preloading
- Top progress bar on navigation
- Full-screen overlay spinner on form submit
- Contact form with validation
- Whitenoise static file serving

## License

Personal project by Xenon Studio.
