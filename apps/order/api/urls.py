from django.urls import path
from . import views

app_name = 'order_api'
urlpatterns = [
    path('cart/', views.CartAPI.as_view(), name='cart'),
]
