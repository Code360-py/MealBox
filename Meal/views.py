import requests
from .models import Bookmark
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def mealCategories():
    url = 'https://www.themealdb.com/api/json/v1/1/categories.php'
    res = requests.get(url).json().get('categories', [])
    return res
    
    
def ChristmasCake():
    url = 'https://www.themealdb.com/api/json/v1/1/search.php?s=cake'
    res = requests.get(url).json().get('meals', [])[:8]
    return res


##############
# Contents
##############

def home(request):
    query = request.GET.get('q', '').strip()
    categories_url = "https://www.themealdb.com/api/json/v1/1/categories.php"
    categories = mealCategories()
    cakes_url = "https://www.themealdb.com/api/json/v1/1/search.php?s=cake"
    cakes = ChristmasCake()
    meals = []
    if query:
        search_url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={query}"
        meals = requests.get(search_url).json().get('meals', [])
    context = {'categories': categories, 'cakes': cakes, 'meals': meals, 'query': query}
    return render(request, 'index.html', context)
    

def Christmas(request):
    return render(request, 'Content/christmas.html')
    
def about(request):
    return render(request, 'Content/about.html')
    
def contact(request):
    return render(request, 'Content/contact.html')
    
def course(request):
    return render(request, 'Content/course.html')
    
def methods(request):
    return render(request, 'Content/methods.html')
    
def support(request):
    return render(request, 'Content/support.html')
    
    
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    return render(request, 'Content/login.html')
    

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
        else:
            messages.error(request, 'Username already exists or password is invalid')
    else:
        form = UserCreationForm()
    return render(request, 'Content/register.html', {'form': form})
        
        
def logout_view(request):
    logout(request)
    return redirect('login')
    
###############    
# Utilities
###############
@login_required
def toggle_bookmark(request):
    if request.method == 'POST':
        meal_id = request.POST.get('meal_id')
        meal_name = request.POST.get('meal_name')
        meal_thumb = request.POST.get('meal_thumb')

        bookmark, created = Bookmark.objects.get_or_create(user=request.user,
            meal_id=meal_id,defaults={'meal_name': meal_name,'meal_thumb': meal_thumb})
        if not created:
            bookmark.delete()
            messages.info(request, 'Bookmark removed')
        else:
            messages.success(request, 'Meal bookmarked')
    return redirect(request.META.get('HTTP_REFERER', 'home'))
    
    
@login_required
def bookmark_list(request):
    bookmarks = Bookmark.objects.filter(user=request.user)
    return render(request, 'Content/bookmarks.html', {'bookmarks': bookmarks})    
    
    
def filterCalegory(request, category):
    url = f'https://www.themealdb.com/api/json/v1/1/filter.php?c={category}'
    meals = requests.get(url).json()['meals']
    return render(request, 'meals.html', {'meals': meals, 'category': category})
        
        
def mealDetails(request, meal_id):
    url = f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}'
    recipe = requests.get(url).json()['meals']
    bookmarked_ids = []
    if request.user.is_authenticated:
        bookmarked_ids = Bookmark.objects.filter(user=request.user).values_list('meal_id', flat=True)
    return render(request, 'meal_view.html', {'recipe': recipe,'bookmarked_ids': bookmarked_ids})