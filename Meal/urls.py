from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('christmas/', views.Christmas, name='christmas'),
    
    path('login/', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('course/', views.course, name='course'),
    path('methods/', views.methods, name='methods'),
    path('support/', views.support, name='support'),
    
    path('bookmarks/', views.bookmark_list, name='bookmarks'),
    path('bookmark/toggle/', views.toggle_bookmark, name='toggle_bookmark'),
    
    path('meal/category/<str:category>', views.filterCalegory, name='category'),
    path('meal/recipe/<int:meal_id>', views.mealDetails, name='recipe'),
]