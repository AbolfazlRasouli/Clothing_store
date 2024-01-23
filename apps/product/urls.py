
from django.urls import path
from .views import home, category,ProductDetailView

urlpatterns = [
    path('', home, name='home'),
    path('category/', category, name='category'),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='detail')

]
