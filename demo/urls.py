from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('users/', views.user_route, name='users'),
    path('transactions/', views.transaction_route, name='transactions'),
    path('transactions/create/', views.create_transaction, name='create_transaction')
]