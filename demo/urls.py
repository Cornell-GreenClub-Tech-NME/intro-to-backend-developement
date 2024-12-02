from django.urls import path
from . import views

urlpatterns = [
    path('api/users/', views.user_route, name='users'),
    path('api/users/<int:id>/', views.get_user_by_id, name='get_user'),
    path('api/users/transactions/', views.transaction_route, name='transactions')
]