
from django.urls import path
from .views import cart_view, show_buy

app_name = "order"
urlpatterns = [
    path('cart/', cart_view, name='cart_view'),
    path('showbuy', show_buy, name='show_buy')
]
