import requests
from datetime import date
from django.shortcuts import render, redirect
from .models import User, Bookmark
from .auth import login_user, logout_user, get_current_user, login_required


API = 'https://www.themealdb.com/api/json/v1/1'


def _get(path, params=None):
    try:
        r = requests.get(f"{API}/{path}", params=params, timeout=10)
        return r.json() or {}
    except Exception:
        return {}


def _ctx(request, **extra):
    ctx = {
        'current_user': get_current_user(request),
        'next_festival': next_festival(),
    }
    ctx.update(extra)
    return ctx


from datetime import date, datetime

def _parse_dob(raw):
    """Return a date or None. Accepts YYYY-MM-DD."""
    raw = (raw or '').strip()
    if not raw:
        return None
    try:
        return datetime.strptime(raw, '%Y-%m-%d').date()
    except ValueError:
        return None



# ----------------------------------------------------------------------
# Next-festival helper
# ----------------------------------------------------------------------
def next_festival():
    """Return dict {key, label, when} for the nearest upcoming festival."""
    today = date.today()
    year = today.year

    DIWALI = {
        2025: date(2025, 10, 20),
        2026: date(2026, 11,  8),
        2027: date(2027, 10, 29),
        2028: date(2028, 10, 17),
        2029: date(2029, 11,  5),
    }

    def diwali_in(y):
        return DIWALI.get(y) or date(y, 11, 1)

    candidates = [
        ('diwali',    'Diwali',    diwali_in(year)),
        ('christmas', 'Christmas', date(year,     12, 25)),
        ('diwali',    'Diwali',    diwali_in(year + 1)),
        ('christmas', 'Christmas', date(year + 1, 12, 25)),
    ]

    upcoming = [c for c in candidates if c[2] >= today]
    if not upcoming:
        return None

    key, label, when = min(upcoming, key=lambda c: c[2])
    days = (when - today).days

    if days == 0:
        when_str = 'today'
    elif days == 1:
        when_str = 'tomorrow'
    elif days <= 30:
        when_str = f'in {days} days'
    else:
        months = max(1, round(days / 30))
        when_str = f'in {months} months'

    return {'key': key, 'label': label, 'when': when_str, 'days': days}


# ----------------------------------------------------------------------
# Seasonal helpers
# ----------------------------------------------------------------------
def is_christmas_season():
    today = date.today()
    return (today.month == 12) or (today.month == 1 and today.day <= 6)


def is_diwali_season():
    today = date.today()
    return (today.month == 10 and today.day >= 15) or \
           (today.month == 11 and today.day <= 15)


def is_birthday_season():
    # Birthdays are year-round
    return True


def _search_recipes(terms, limit=24):
    """Aggregate searches, dedupe, return up to `limit` recipes."""
    seen = set()
    out = []
    for term in terms:
        meals = _get('search.php', {'s': term}).get('meals') or []
        for m in meals:
            mid = m.get('idMeal')
            if not mid or mid in seen:
                continue
            seen.add(mid)
            out.append(m)
            if len(out) >= limit:
                return out
    return out


def christmas_recipes(limit=24):
    return _search_recipes(['christmas', 'turkey', 'pudding', 'cake'], limit)


def diwali_recipes(limit=24):
    return _search_recipes(['indian', 'curry', 'lamb', 'chicken'], limit)


def birthday_recipes(limit=24):
    return _search_recipes(['cake', 'chocolate', 'dessert', 'pudding'], limit)


# ----------------------------------------------------------------------
# Content pages
# ----------------------------------------------------------------------
def home(request):
    query = request.GET.get('q', '').strip()
    meals = []
    if query:
        meals = _get('search.php', {'s': query}).get('meals') or []

    categories = _get('categories.php').get('categories', [])

    user = get_current_user(request)
    return render(request, 'index.html', _ctx(
        request,
        categories=categories,
        meals=meals,
        query=query,
        show_christmas=is_christmas_season(),
        show_diwali=is_diwali_season(),
        show_birthday=is_birthday_season(),
        personal_birthday=(user.is_birthday_today() if user else False),
        active_tab='home',
    ))


def about(request):
    return render(request, 'Content/about.html', _ctx(request, active_tab='home'))


def contact(request):
    success = False
    error = None

    if request.method == 'POST':
        name    = request.POST.get('name', '').strip()
        email   = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        if not name or not email or not message:
            error = 'All fields are required'
        elif '@' not in email or '.' not in email.split('@')[-1]:
            error = 'Please enter a valid email address'
        elif len(message) < 10:
            error = 'Message must be at least 10 characters'
        else:
            success = True

    return render(request, 'Content/contact.html', _ctx(
        request,
        success=success,
        error=error,
        active_tab='home',
    ))


def christmas(request):
    return render(request, 'Content/christmas.html', _ctx(
        request,
        recipes=christmas_recipes(24),
        in_season=is_christmas_season(),
        active_tab='home',
    ))


def diwali(request):
    return render(request, 'Content/diwali.html', _ctx(
        request,
        recipes=diwali_recipes(24),
        in_season=is_diwali_season(),
        active_tab='home',
    ))


def birthday(request):
    return render(request, 'Content/birthday.html', _ctx(
        request,
        recipes=birthday_recipes(24),
        in_season=True,
        active_tab='home',
    ))


# ----------------------------------------------------------------------
# Auth
# ----------------------------------------------------------------------
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = User.objects.filter(username=username, is_active=True).first()
        if user and user.check_password(password):
            login_user(request, user)
            return redirect('home')

        return render(request, 'Content/login.html', _ctx(
            request, error='Invalid username or password', active_tab='account'))

    if get_current_user(request):
        return redirect('home')

    return render(request, 'Content/login.html', _ctx(request, active_tab='account'))


def register(request):
    if request.method == 'POST':
        username  = request.POST.get('username', '').strip()
        email     = request.POST.get('email', '').strip()
        password  = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        dob_raw   = request.POST.get('date_of_birth', '').strip()
        dob       = _parse_dob(dob_raw)

        error = None
        if not username or not email or not password:
            error = 'All fields are required'
        elif password != password2:
            error = 'Passwords do not match'
        elif len(password) < 6:
            error = 'Password must be at least 6 characters'
        elif User.objects.filter(username=username).exists():
            error = 'Username already taken'
        elif User.objects.filter(email=email).exists():
            error = 'Email already registered'
        elif dob_raw and dob is None:
            error = 'Date of birth must be in YYYY-MM-DD format'
        elif dob and dob > date.today():
            error = 'Date of birth cannot be in the future'

        if error:
            return render(request, 'Content/register.html', _ctx(
                request, error=error,
                username=username, email=email, date_of_birth=dob_raw,
                active_tab='account'))

        user = User(username=username, email=email, date_of_birth=dob)
        user.set_password(password)
        user.save()

        login_user(request, user)
        return redirect('home')

    return render(request, 'Content/register.html', _ctx(request, active_tab='account'))


def logout_view(request):
    logout_user(request)
    return redirect('login')


@login_required
def save_dob(request):
    user = get_current_user(request)
    if request.method == 'POST':
        dob_raw = request.POST.get('date_of_birth', '').strip()
        dob = _parse_dob(dob_raw)

        if dob_raw and dob is None:
            error = 'Date must be in YYYY-MM-DD format'
        elif dob and dob > date.today():
            error = 'Date of birth cannot be in the future'
        else:
            user.date_of_birth = dob
            user.save()
            return redirect('account')

        bookmarks = Bookmark.objects.filter(user=user)
        return render(request, 'Content/account.html', _ctx(
            request,
            user=user,
            bookmark_count=bookmarks.count(),
            recent_bookmarks=list(bookmarks[:3]),
            age=user.age(),
            is_birthday_today=user.is_birthday_today(),
            dob_error=error,
            active_tab='account',
        ))

    return redirect('account')


# ----------------------------------------------------------------------
# Account
# ----------------------------------------------------------------------
@login_required
def account(request):
    user = get_current_user(request)
    bookmarks = Bookmark.objects.filter(user=user)
    recent = list(bookmarks[:3])

    return render(request, 'Content/account.html', _ctx(
        request,
        user=user,
        bookmark_count=bookmarks.count(),
        recent_bookmarks=recent,
        age=user.age(),
        is_birthday_today=user.is_birthday_today(),
        active_tab='account',
    ))


# ----------------------------------------------------------------------
# Bookmarks
# ----------------------------------------------------------------------
@login_required
def toggle_bookmark(request):
    if request.method == 'POST':
        user = get_current_user(request)
        meal_id    = request.POST.get('meal_id', '').strip()
        meal_name  = request.POST.get('meal_name', '').strip()
        meal_thumb = request.POST.get('meal_thumb', '').strip()

        if not meal_id or not meal_name:
            return redirect(request.META.get('HTTP_REFERER') or 'home')

        bookmark, created = Bookmark.objects.get_or_create(
            user=user, meal_id=meal_id,
            defaults={'meal_name': meal_name, 'meal_thumb': meal_thumb},
        )
        if not created:
            bookmark.delete()

    return redirect(request.META.get('HTTP_REFERER') or 'home')


@login_required
def bookmark_list(request):
    user = get_current_user(request)
    bookmarks = Bookmark.objects.filter(user=user)
    return render(request, 'Content/bookmarks.html', _ctx(
        request, bookmarks=bookmarks, active_tab='bookmarks'))


# ----------------------------------------------------------------------
# Meals
# ----------------------------------------------------------------------
def filterCalegory(request, category):
    meals = _get('filter.php', {'c': category}).get('meals') or []
    return render(request, 'meals.html', _ctx(
        request, meals=meals, category=category, active_tab='home'))


def mealDetails(request, meal_id):
    data = _get('lookup.php', {'i': meal_id}).get('meals') or []
    recipe = data[0] if data else None

    ingredients = []
    if recipe:
        for i in range(1, 21):
            name    = (recipe.get(f'strIngredient{i}') or '').strip()
            measure = (recipe.get(f'strMeasure{i}') or '').strip()
            if name:
                ingredients.append({'name': name, 'measure': measure})

    user = get_current_user(request)
    bookmarked_ids = []
    if user:
        bookmarked_ids = list(
            Bookmark.objects.filter(user=user).values_list('meal_id', flat=True)
        )

    return render(request, 'meal_view.html', _ctx(
        request,
        recipe=recipe,
        ingredients=ingredients,
        bookmarked_ids=bookmarked_ids,
        active_tab='home'))


# ----------------------------------------------------------------------
# Delete account
# ----------------------------------------------------------------------
@login_required
def delete_account(request):
    user = get_current_user(request)

    if request.method == 'POST':
        password = request.POST.get('password', '')
        confirm  = request.POST.get('confirm', '').strip()

        if confirm != 'DELETE':
            return render(request, 'Content/delete_account.html', _ctx(
                request,
                user=user,
                error='Type DELETE (all caps) to confirm.',
                active_tab='account',
            ))

        if not user.check_password(password):
            return render(request, 'Content/delete_account.html', _ctx(
                request,
                user=user,
                error='Incorrect password.',
                active_tab='account',
            ))

        # Log out first, then delete the user (bookmarks cascade-delete)
        logout_user(request)
        user.delete()
        return redirect('home')

    return render(request, 'Content/delete_account.html', _ctx(
        request,
        user=user,
        active_tab='account',
    ))


# ----------------------------------------------------------------------
# Search
# ----------------------------------------------------------------------
def search(request):
    query = request.GET.get('q', '').strip()
    meals = []
    if query:
        meals = _get('search.php', {'s': query}).get('meals') or []

    return render(request, 'search.html', _ctx(
        request,
        query=query,
        meals=meals,
        active_tab='search',
    ))
