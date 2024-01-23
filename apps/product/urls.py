
from django.urls import path
from .views import home, category, detail

urlpatterns = [
    path('', home, name='home'),
    path('category/', category, name='category'),
    path('detail/<slug:slug>/', detail)

]
