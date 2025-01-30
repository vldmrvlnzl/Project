from django.urls import path
from .views import (
    HomePageView,
    AboutPageView,
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductListView,
    ProductUpdateView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("product_list/", ProductListView.as_view(), name="product_list"),
    path("product_detail/<int:pk>", ProductDetailView.as_view(), name="product_detail"),
    path("product_create/create", ProductCreateView.as_view(), name="product_create"),
    path("product_update/<int:pk>/edit", ProductUpdateView.as_view(), name="product_update"),
    path("product_delete/<int:pk>/delete", ProductDeleteView.as_view(), name="product_delete"),
]
