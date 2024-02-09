from django.urls import path
from . import views

app_name = 'order_api'
urlpatterns = [
    path('profile/', views.ProfileAPI.as_view(), name='profile'),
]
