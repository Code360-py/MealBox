from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('random/', views.random_recipe, name='random_recipe'),

    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('account/', views.account, name='account'),
    path('account/delete/', views.delete_account, name='delete_account'),
    path('account/dob/', views.save_dob, name='save_dob'),

    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    path('christmas/', views.christmas, name='christmas'),
    path('diwali/', views.diwali, name='diwali'),
    path('birthday/', views.birthday, name='birthday'),

    path('bookmarks/', views.bookmark_list, name='bookmarks'),
    path('bookmark/toggle/', views.toggle_bookmark, name='toggle_bookmark'),

    path('meal/category/<str:category>/', views.filterCalegory, name='category'),
    path('meal/recipe/<int:meal_id>/', views.mealDetails, name='recipe'),
]
