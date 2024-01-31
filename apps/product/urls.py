
from django.urls import path
from .views import ProductDetailView, HomePage, CategoryProductListView, CommentCreateView, item_search, LikeProductView

app_name = "product"
urlpatterns = [
    path('', HomePage.as_view(), name='home_page'),
    path('category/<int:pk>/', CategoryProductListView.as_view(), name='category_product'),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='detail_product'),
    path('comment/<int:details_id>/', CommentCreateView.as_view(), name='comment_create'),
    path('search/', item_search, name='item_search'),
    path('like/<int:pk>/', LikeProductView.as_view(), name='like_product')

]
