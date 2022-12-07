from django.shortcuts import render, redirect
from django.views import generic as views
from . forms import CustomAuthenticationForm, SignUpForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy


UserModel = get_user_model()

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = CustomAuthenticationForm


class UserCreationView(views.CreateView):
    template_name = 'users/register.html'
    form_class = SignUpForm
    success_url=reverse_lazy('home')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result

    
class UserLogoutView(LogoutView):
    pass
