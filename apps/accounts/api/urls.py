from django.urls import path
from . import views

app_name = 'order_api'
urlpatterns = [
    path('profile/', views.ProfileAPI.as_view(), name='profile'),
    path('Addressshoow/', views.AddressApi.as_view(), name='address_show'),
    path('detailaddress/<int:pk>/', views.DetailAddress.as_view(), name='detail_address')
]
