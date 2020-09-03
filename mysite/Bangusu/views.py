from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.views.generic import ListView, DetailView, View
from .models import Product, OrderItem, Order
from django.db.models import F


def start_page(request):
    return render(request, "Bangusu/start_page.html", {})


class CategoryM:
    def get_category(self):
        return Product.objects.all()


class WomanPage(CategoryM, ListView):
    queryset = Product.objects.filter(available=True, for_woman=True)
    template_name = 'Bangusu/w_page.html'
    context_object_name = 'image'


class ManPage(CategoryM, ListView):
    queryset = Product.objects.filter(available=True, for_man=True)
    template_name = 'Bangusu/m_page.html'
    context_object_name = 'image'


class AllPage(CategoryM, ListView):
    queryset = Product.objects.filter(available=True)
    template_name = 'Bangusu/all_page.html'
    context_object_name = 'image'


class ProductDetail(DetailView):
    queryset = Product.objects.all()
    slug_field = "slug"
    context_object_name = 'image'


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'Bangusu/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")


class FilterCategory(CategoryM, ListView):
    def get_queryset(self):
        queryset = Product.objects.filter(categryyn__in=self.request.GET.getlist('categryyn'))
        return queryset

    template_name = 'Bangusu/all_page.html'

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # chek if the order item in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.stock = F('stock') + 1
            order_item.save()
            messages.info(request, "Another one!")
            return redirect("bnsu:product_detail", slug=slug)
        else:
            order.items.add(order_item)
            messages.info(request, "Added on your cart!")
            return redirect("bnsu:product_detail", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user,
            ordered_date=ordered_date
        )
        order.items.add(order_item)
        messages.info(request, "Added on your cart!")
        return redirect("bnsu:product_detail", slug=slug)

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # chek if the order item in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "Removed from your cart!")
            return redirect("bnsu:order-summary")
        else:
            # add a message "you order douse not contain the item"
            messages.info(request, "This stuff was not in your cart!")
            return redirect("bnsu:product_detail", slug=slug)
    else:
        # add a message "you doesn't have an order"
        messages.info(request, "You do not have an active order!")
        return redirect("bnsu:product_detail", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # chek if the order item in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.stock > 1:
                order_item.stock = F('stock') - 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated!")
            return redirect("bnsu:order-summary")
        else:
            # add a message "you order douse not contain the item"
            messages.info(request, "This stuff was not in your cart!")
            return redirect("bnsu:order-summary", slug=slug)
    else:
        # add a message "you doesn't have an order"
        messages.info(request, "You do not have an active order!")
        return redirect("bnsu:order-summary", slug=slug)

@login_required
def add_single_item_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # chek if the order item in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.stock = F('stock') + 1
            order_item.save()
            messages.info(request, "Another one!")
        else:
            order.items.add(order_item)
            messages.info(request, "Added on your cart!")
            return redirect("bnsu:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user,
            ordered_date=ordered_date
        )
        order.items.add(order_item)
        messages.info(request, "Added on your cart!")
    return redirect("bnsu:order-summary")