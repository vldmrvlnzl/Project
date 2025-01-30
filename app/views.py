from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from app.models import Product
from django.urls import reverse_lazy


# Create your views here.
class HomePageView(TemplateView):
    template_name = "app/home.html"


class AboutPageView(TemplateView):
    template_name = "app/about.html"


class ProductListView(ListView):
    model = Product
    context_object_name = "products"
    template_name = "app/product_list.html"


class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"
    template_name = "app/product_detail.html"


class ProductCreateView(CreateView):
    model = Product
    fields = ["name", "description", "price", "stock_quantity"]
    template_name = "app/product_create.html"


class ProductUpdateView(UpdateView):
    model = Product
    fields = ["name", "description", "price", "stock_quantity"]
    template_name = "app/product_update.html"


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "app/product_delete.html"
    success_url = reverse_lazy("product_list")
