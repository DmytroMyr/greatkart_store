from django.urls import path
from . import views


urlpatterns = [
    path('registration/', views.registration_view, name='registration'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('', views.dashboard_view, name='dashboard'),
    path('my_orders/', views.my_orders_view, name='my_orders'),
    path('order_detail/<int:order_id>/', views.order_detail_view, name='order_detail'),
]