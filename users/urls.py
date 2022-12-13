from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('register/', views.UserCreationView.as_view(), name='register'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile', views.edit_profile, name='edit-profile'),
    path('delete_profile', views.delete_profile, name='delete-profile'),
    path('delete_profile_final', views.delete_profile_final, name='delete-profile-final'),
]