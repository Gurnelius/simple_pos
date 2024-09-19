from django.contrib.auth.views import LoginView, LogoutView

from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import UserRegistrationForm


class UserSignupView(FormView):
    template_name = 'accounts/signup.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form is invalid")
        print(f"Form errors: {form.errors}")
        return super().form_invalid(form)

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'  # Organized under accounts subfolder

    def get_success_url(self):
        return reverse_lazy('product_list')

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')
