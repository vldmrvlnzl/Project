from django.urls import path
from . import views
from .views import (
    AccountDeleteView,
    CartListView,
    CheckoutListView,
    HomePageView,
    AboutPageView,
    OrderDetailsView,
    OrderView,
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductListView,
    ProductUpdateView,
    ProfileUpdateView,
    ProfileView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("product_list/", ProductListView.as_view(), name="product_list"),
    path("product_detail/<int:pk>", ProductDetailView.as_view(), name="product_detail"),
    path("product_create/create", ProductCreateView.as_view(), name="product_create"),
    path(
        "product_update/<int:pk>/edit",
        ProductUpdateView.as_view(),
        name="product_update",
    ),
    path(
        "product_delete/<int:pk>/delete",
        ProductDeleteView.as_view(),
        name="product_delete",
    ),
    path('cart/', CartListView.as_view(), name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', CheckoutListView.as_view(), name='checkout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('profile/delete/', AccountDeleteView.as_view(), name='account_delete'),
    path('order/', OrderView.as_view(), name='order'),
    path('order_details/<int:pk>/', OrderDetailsView.as_view(), name='order_details')

    ]
