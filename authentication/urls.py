from . import views
from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import LoginView

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(next_page='/'), name='logout'),
    path('change-password', views.change_password, name='change_password'),
    path('reset-password', views.reset_password, name='reset_password'),
    path(
        'complete-password-reset/<uidb64>/<token>',
        views.complete_password_reset,
        name="complete_password_reset",
    ),
]