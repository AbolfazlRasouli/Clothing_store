
from django.urls import path
from .views import ProductDetailView, HomePage

app_name = "product"
urlpatterns = [
    path('', HomePage.as_view(), name='home_page'),
    # path('category/', category, name='category'),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='detail')

]
