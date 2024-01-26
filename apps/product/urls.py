
from django.urls import path
from .views import ProductDetailView, HomePage, CategoryDetailView, CommentCreateView

app_name = "product"
urlpatterns = [
    path('', HomePage.as_view(), name='home_page'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_product'),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='detail_product'),
    path('comment/<int:details_id>/', CommentCreateView.as_view(), name='comment_create')

]
