from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from app.models import CartItem, Order, OrderItem, Payment, Product, Cart
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm


# Create your views here.

User = get_user_model()

@method_decorator(login_required, name='dispatch')
class ProfileView(DetailView):
    model = User
    template_name = 'app/profile.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user  

@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    model = User
    form_class = UserChangeForm
    template_name = 'app/profile_update.html'
    success_url = reverse_lazy('profile')  

    def get_object(self):
        return self.request.user 

@method_decorator(login_required, name='dispatch')
class AccountDeleteView(DeleteView):
    model = User
    template_name = 'app/account_delete.html'
    success_url = reverse_lazy('home')  
    def get_object(self):
        return self.request.user  

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect("cart")

def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)

    for item in cart_items:
        item.total_price = item.product.price * item.quantity

    return render(request, "app/cart.html", {"cart_items": cart_items})



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
    template_name = 'app/product_detail.html'
    context_object_name = 'product'

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        quantity = int(request.POST.get('quantity', 1)) 
        
        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
        )

        cart_item.quantity += quantity 
        cart_item.save()

        return redirect('cart')

class ProductCreateView(CreateView):
    model = Product
    fields = ["name", "image", "description", "price", "stock_quantity"]
    template_name = "app/product_create.html"


class ProductUpdateView(UpdateView):
    model = Product
    fields = ["name", "description", "price", "stock_quantity"]
    template_name = "app/product_update.html"


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "app/product_delete.html"
    success_url = reverse_lazy("product_list")

class CartListView(ListView):
    model = CartItem
    template_name = "app/cart.html"
    context_object_name = "cart_items"

    def get_queryset(self):
        cart = Cart.objects.get(user=self.request.user)
        return cart.items.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_cart_price = 0

        for item in context["cart_items"]:
            item.total_price = item.product.price * item.quantity
            total_cart_price += item.total_price

        context["total_cart_price"] = total_cart_price
        return context

    def post(self, request, *args, **kwargs):
        delete_item_id = request.POST.get("delete_item")

        if delete_item_id:
            cart_item = get_object_or_404(CartItem, id=delete_item_id)
            cart_item.delete()

        return redirect("cart")

class CheckoutListView(ListView):
    model = CartItem
    template_name = 'app/checkout.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user, ordered=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = context['cart_items']
        item_totals = [
            {
                'item': item,
                'total_price': item.product.price * item.quantity,
            }
            for item in cart_items
        ]
        total_cart_price = sum(item['total_price'] for item in item_totals)
        context['item_totals'] = item_totals
        context['total_cart_price'] = total_cart_price
        return context

    def post(self, request, *args, **kwargs):
        cart_items = CartItem.objects.filter(cart__user=request.user, ordered=False)
        order = Order.objects.create(user=request.user, total_ammount=0)  # Create a new order
        total_amount = 0
        
        for item in cart_items:
            item.ordered = True
            item.save()
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
            total_amount += item.product.price * item.quantity
        
        order.total_ammount = total_amount
        order.save()

        Payment.objects.create(order=order, amount=total_amount, payment_method="Credit Card", status="Paid")
        
        return redirect('order_details', pk=order.id)

class OrderView(ListView):
    model = CartItem
    template_name = 'app/order.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = context['cart_items']
        context['item_totals'] = [
            {'item': item, 'total_price': item.product.price * item.quantity}
            for item in cart_items
        ]
        context['total_cart_price'] = sum(item['total_price'] for item in context['item_totals'])
        return context

class OrderDetailsView(DetailView):
    model = Order
    template_name = 'app/order_details.html'
    context_object_name = 'order'

    def get_object(self):
        # Using the primary key (pk) from the URL pattern
        order_id = self.kwargs.get('pk')  # Corrected from 'order_id' to 'pk'
        return get_object_or_404(Order, pk=order_id)  # Using pk here instead of id

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = context['order']
        order_items = OrderItem.objects.filter(order=order)

        item_totals = [
            {
                'item': item,
                'total_price': item.product.price * item.quantity,
            }
            for item in order_items
        ]
        
        total_order_price = sum(item['total_price'] for item in item_totals)

        context['item_totals'] = item_totals
        context['total_order_price'] = total_order_price
        return context
