from django.urls import path
from . import views


urlpatterns = [
    path('registration/', views.registration_view, name='registration'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]