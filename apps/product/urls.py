
from django.urls import path
from .views import ProductDetailView, HomePage

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    # path('category/', category, name='category'),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='detail')

]
