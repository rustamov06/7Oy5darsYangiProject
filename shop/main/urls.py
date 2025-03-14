from django.urls import path
from .views import IndexView, ProductDetailView, CategoryDetailView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path("product/<slug:slug>/", ProductDetailView.as_view(), name="product_detail"),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
]