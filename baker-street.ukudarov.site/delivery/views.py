from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, get_user_model
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, View, TemplateView
from django.contrib.auth.models import Group
from django.shortcuts import get_list_or_404, get_object_or_404
import datetime

from products.models import *
from users.models import *
from carts.models import *
from orders.models import *

from .forms import *


class DeliveryBaseView(View):

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated == True:
            datetoday = datetime.date.today()
            deliveryman = Deliveryman.objects.get(user=request.user)
            if request.user.is_staff == True:
                shops = ShopBuyer.objects.all()
            elif Deliveryman.objects.filter(user=request.user):
                shops = ShopBuyer.objects.filter(deliveryman=deliveryman)
            elif not Deliveryman.objects.filter(user=request.user):
                return redirect("/")
            paginator = Paginator(shops, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            if DeliveryForDay.objects.filter(user=request.user, created_at=datetime.date.today()):
                delivery_for_day = DeliveryForDay.objects.get(user=request.user, created_at=datetime.date.today())
                for item in shops:
                    if not ShopDeliveryForDay.objects.filter(delivery=delivery_for_day, shop=item):
                        ShopDeliveryForDay.objects.create(delivery=delivery_for_day, shop=item)
            else:
                delivery_for_day = DeliveryForDay.objects.create(user=request.user)
                for item in shops:
                    ShopDeliveryForDay.objects.create(delivery=delivery_for_day, shop=item)
            shops_delivery_for_day = ShopDeliveryForDay.objects.filter(delivery=delivery_for_day)

            realization_orders_kaspi = Order.objects.filter(user=request.user, finish_making=True, created_at=datetime.date.today(), buying_type='realization').order_by('-id')
            orders = Order.objects.filter(user=request.user, finish_making=True, created_at=datetime.date.today(), buying_type='simple', pay='cash').order_by('-id')
            orders_kaspi = Order.objects.filter(user=request.user, finish_making=True, created_at=datetime.date.today(), buying_type='simple', pay='kaspi').order_by('-id')

            total_realization_orders_kaspi = 0
            total_orders = 0
            total_orders_kaspi = 0

            for item in realization_orders_kaspi:
                total_realization_orders_kaspi += item.total_price

            for item in orders:
                total_orders += item.total_price

            for item in orders_kaspi:
                total_orders_kaspi += item.total_price

            context = {
                'total_realization_orders_kaspi': total_realization_orders_kaspi,
                'total_orders': total_orders,
                'total_orders_kaspi': total_orders_kaspi,
                'datetoday': datetoday,
                'shops_delivery_for_day': shops_delivery_for_day,
                'page_obj': page_obj
            }
            return render(request, 'delivery/base.html', context)
        else:
            return redirect("/delivery/login")


class ChangeStatusDelivery(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            if kwargs.get('status') == 0:
                ShopDeliveryForDay.objects.filter(id=kwargs.get('id')).update(delivered=False)
            elif kwargs.get('status') == 1:
                ShopDeliveryForDay.objects.filter(id=kwargs.get('id')).update(delivered=True)

            return redirect("delivery_base")
        elif request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            if kwargs.get('status') == 0:
                ShopDeliveryForDay.objects.filter(id=kwargs.get('id')).update(delivered=False)
            elif kwargs.get('status') == 1:
                ShopDeliveryForDay.objects.filter(id=kwargs.get('id')).update(delivered=True)

            return redirect("delivery_base")
        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")
        else:
            return redirect("/delivery/login")


class DeliveryLoginView(View):

    def get(self, request, *args, **kwargs):
        form = DeliveryLoginForm(request.POST or None)
        context = {
            'form': form,
        }
        if request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            return redirect("/delivery")
        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")
        else:
            return render(request, 'delivery/login.html', context)


    def post(self, request, *args, **kwargs):
        form = DeliveryLoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.get(username=username)
            if Deliveryman.objects.filter(user=user):
                user = authenticate(
                    username=username, password=password
                )
                if user:
                    login(request, user)
                    return HttpResponseRedirect('/delivery')
            else:
                user = authenticate(
                    username=username, password=password
                )
                if user:
                    login(request, user)
                    return HttpResponseRedirect('/')
        context = {
            'form': form,
        }
        return render(request, 'delivery/login.html', context)


class ShopContactDetailView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            shop = ShopBuyer.objects.get(id=kwargs.get('id'))
            context = {
                'shop': shop
            }
            return render(request, 'delivery/shop_contact_detail.html', context)
        elif request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            deliveryman = Deliveryman.objects.get(user=request.user)
            shop = ShopBuyer.objects.get(id=kwargs.get('id'), deliveryman=deliveryman)
            context = {
                'shop': shop
            }
            return render(request, 'delivery/shop_contact_detail.html', context)
        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")
        else:
            return redirect("/delivery/login")


class DeliverymanProfileView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            deliveryman = Deliveryman.objects.get(user=request.user)
            context = {
                'deliveryman': deliveryman,
            }
            return render(request, 'delivery/profile.html', context)
        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")
        else:
            return redirect("/delivery/login")


class EditDeliverymanProfileView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            deliveryman = Deliveryman.objects.get(user=request.user)
            form = EditDeliverymanProfileForm(request.POST or None, instance=deliveryman)
            context = {
                'form': form,
                'deliveryman': deliveryman,
            }
            return render(request, 'delivery/edit_profile.html', context)
        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")
        else:
            return redirect("/delivery/login")

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            deliveryman = Deliveryman.objects.get(user=request.user)

            if request.method == "POST":
                form = EditDeliverymanProfileForm(request.POST or None, instance=deliveryman)
                if form.is_valid():
                    form.save()
                    return redirect('delivery_profile')
            else:
                form = EditDeliverymanProfileForm(request.POST or None, instance=deliveryman)

            context = {
                'form': form,
                'deliveryman': deliveryman
            }
            return render(request, 'delivery/edit_profile.html', context)

        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")

        else:
            return redirect("/delivery/login")


class EditShopContactView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            shop = ShopBuyer.objects.get(id=kwargs.get('id'))
            form = EditShopContactForm(request.POST or None, instance=shop)
            context = {
                'form': form,
                'shop': shop
            }
            return render(request, 'delivery/edit_shop_contact.html', context)
        elif request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            deliveryman = Deliveryman.objects.get(user=request.user)
            shop = ShopBuyer.objects.get(id=kwargs.get('id'), deliveryman=deliveryman)
            form = EditShopContactForm(request.POST or None, instance=shop)
            context = {
                'form': form,
                'shop': shop
            }
            return render(request, 'delivery/edit_shop_contact.html', context)
        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")
        else:
            return redirect("/delivery/login")

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            shop = ShopBuyer.objects.get(id=kwargs.get('id'))

            if request.method == "POST":
                form = EditShopContactForm(request.POST or None, instance=shop)
                if form.is_valid():
                    form.save()
                    return redirect('shop_detail', shop.id)
            else:
                form = EditShopContactForm(request.POST or None, instance=shop)

            context = {
                'form': form,
                'shop': shop
            }
            return render(request, 'delivery/edit_shop_contact.html', context)
        elif request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            deliveryman = Deliveryman.objects.get(user=request.user)
            shop = ShopBuyer.objects.get(id=kwargs.get('id'), deliveryman=deliveryman)


            if request.method == "POST":
                form = EditShopContactForm(request.POST or None, instance=shop)
                if form.is_valid():
                    form.save()
                    return redirect('shop_detail', shop.id)
            else:
                form = EditShopContactForm(request.POST or None, instance=shop)

            context = {
                'form': form,
                'shop': shop
            }
            return render(request, 'delivery/edit_shop_contact.html', context)
        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")
        else:
            return redirect("/delivery/login")


class EditShopAdminContactView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            shop = ShopBuyer.objects.get(id=kwargs.get('id'))
            shop_admin = ShopAdministrator.objects.get(id=shop.customer.id)
            form = EditShopAdminContactForm(request.POST or None, instance=shop_admin)
            context = {
                'form': form,
                'shop': shop
            }
            return render(request, 'delivery/edit_shop_admin_contact.html', context)

        elif request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            deliveryman = Deliveryman.objects.get(user=request.user)
            shop = ShopBuyer.objects.get(id=kwargs.get('id'), deliveryman=deliveryman)
            shop_admin = ShopAdministrator.objects.get(id=shop.customer.id)
            form = EditShopAdminContactForm(request.POST or None, instance=shop_admin)
            context = {
                'form': form,
                'shop': shop
            }
            return render(request, 'delivery/edit_shop_admin_contact.html', context)
        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")
        else:
            return redirect("/delivery/login")

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            shop = ShopBuyer.objects.get(id=kwargs.get('id'))
            shop_admin = ShopAdministrator.objects.get(id=shop.customer.id)

            if request.method == "POST":
                form = EditShopAdminContactForm(request.POST or None, instance=shop_admin)
                if form.is_valid():
                    form.save()
                    return redirect('shop_detail', shop.id)
            else:
                form = EditShopAdminContactForm(request.POST or None, instance=shop_admin)

            context = {
                'form': form,
                'shop': shop
            }
            return render(request, 'delivery/edit_shop_admin_contact.html', context)
        elif request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            deliveryman = Deliveryman.objects.get(user=request.user)
            shop = ShopBuyer.objects.get(id=kwargs.get('id'), deliveryman=deliveryman)
            shop_admin = ShopAdministrator.objects.get(id=shop.customer.id)


            if request.method == "POST":
                form = EditShopAdminContactForm(request.POST or None, instance=shop_admin)
                if form.is_valid():
                    form.save()
                    return redirect('shop_detail', shop.id)
            else:
                form = EditShopAdminContactForm(request.POST or None, instance=shop_admin)

            context = {
                'form': form,
                'shop': shop
            }
            return render(request, 'delivery/edit_shop_admin_contact.html', context)
        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")
        else:
            return redirect("/delivery/login")

#Заказы
class ShopOrdersDetailView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            shop = ShopBuyer.objects.get(id=kwargs.get('id'))
            orders = Order.objects.filter(buyer_shop=shop, finish_making=True).order_by('-id')
            order_products = OrderProduct.objects.filter(order__in=orders).order_by('-id')

            context = {
                'order_products': order_products,
                'orders': orders,
                'shop': shop
            }
            return render(request, 'delivery/shop_orders_detail.html', context)
        elif request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            deliveryman = Deliveryman.objects.get(user=request.user)
            shop = ShopBuyer.objects.get(id=kwargs.get('id'), deliveryman=deliveryman)
            orders = Order.objects.filter(buyer_shop=shop, finish_making=True).order_by('-id')
            order_products = OrderProduct.objects.filter(order__in=orders).order_by('-id')

            context = {
                'order_products': order_products,
                'orders': orders,
                'shop': shop
            }
            return render(request, 'delivery/shop_orders_detail.html', context)
        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")
        else:
            return redirect("/delivery/login")


class MakeOrderChoiceView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            shop = ShopBuyer.objects.get(id=kwargs.get('id'))
            prepared_products_per_day = PreparedProductsPerDay.objects.get(created_at=datetime.date.today())
            prepared_products = PreparedProduct.objects.filter(prepared_products_p_d=prepared_products_per_day)
            categories = Category.objects.all()
            products = Product.objects.all()

            if not Order.objects.filter(user=request.user, buyer_shop=shop, finish_making=False, created_at=datetime.date.today()):
                order = Order.objects.create(
                                            user=request.user,
                                            role='deliveryman',
                                            buyer_shop=shop
                                            )
            else:
                order = Order.objects.get(
                                            user=request.user,
                                            role='deliveryman',
                                            buyer_shop=shop,
                                            finish_making=False,
                                            created_at=datetime.date.today()
                                            )
            order_products = OrderProduct.objects.filter(order=order)
            context = {
                'order': order,
                'categories': categories,
                'prepared_products': prepared_products,
                'order_products': order_products,
                'products': products,
                'shop': shop
            }
            return render(request, 'delivery/order_choice.html', context)
        elif request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            deliveryman = Deliveryman.objects.get(user=request.user)
            shop = ShopBuyer.objects.get(id=kwargs.get('id'), deliveryman=deliveryman)
            prepared_products_per_day = PreparedProductsPerDay.objects.get(created_at=datetime.date.today())
            prepared_products = PreparedProduct.objects.filter(prepared_products_p_d=prepared_products_per_day)
            categories = Category.objects.all()
            products = Product.objects.all()

            if not Order.objects.filter(user=request.user, buyer_shop=shop, finish_making=False, created_at=datetime.date.today()):
                order = Order.objects.create(
                                            user=request.user,
                                            role='deliveryman',
                                            buyer_shop=shop
                                            )
            else:
                order = Order.objects.get(
                                            user=request.user,
                                            role='deliveryman',
                                            buyer_shop=shop,
                                            finish_making=False,
                                            created_at=datetime.date.today()
                                            )
            order_products = OrderProduct.objects.filter(order=order)
            context = {
                'order': order,
                'categories': categories,
                'prepared_products': prepared_products,
                'order_products': order_products,
                'products': products,
                'shop': shop
            }
            return render(request, 'delivery/order_choice.html', context)
        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")
        else:
            return redirect("/delivery/login")


class CompleteOrderView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            shop = ShopBuyer.objects.get(id=kwargs.get('id'))
            order = Order.objects.get(user=request.user,
                                      role='deliveryman',
                                      buyer_shop=shop,
                                      finish_making=False,
                                      created_at=datetime.date.today())
            form = CompleteOrderForm(request.POST or None, instance=order)
            order_products = OrderProduct.objects.filter(order=order)
            total_price = 0
            for item in order_products:
                order_product = item.qty * item.product.price
                total_price += order_product

            context = {
                'total_price': total_price,
                'order_products': order_products,
                'form': form,
                'order': order,
                'shop': shop
            }
            return render(request, 'delivery/order_complete.html', context)
        elif request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            deliveryman = Deliveryman.objects.get(user=request.user)
            shop = ShopBuyer.objects.get(id=kwargs.get('id'), deliveryman=deliveryman)
            order = Order.objects.get(user=request.user,
                                      role='deliveryman',
                                      buyer_shop=shop,
                                      finish_making=False,
                                      created_at=datetime.date.today())
            form = CompleteOrderForm(request.POST or None, instance=order)
            order_products = OrderProduct.objects.filter(order=order)
            total_price = 0
            for item in order_products:
                order_product = item.qty * item.product.price
                total_price += order_product

            context = {
                'total_price': total_price,
                'order_products': order_products,
                'form': form,
                'order': order,
                'shop': shop
            }
            return render(request, 'delivery/order_complete.html', context)
        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")
        else:
            return redirect("/delivery/login")

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            shop = ShopBuyer.objects.get(id=kwargs.get('id'))
            order = Order.objects.get(user=request.user,
                                      role='deliveryman',
                                      buyer_shop=shop,
                                      finish_making=False,
                                      created_at=datetime.date.today())

            order_products = OrderProduct.objects.filter(order=order)
            prepared_products_per_day = PreparedProductsPerDay.objects.get(created_at=datetime.date.today())
            prepared_products = PreparedProduct.objects.filter(prepared_products_p_d=prepared_products_per_day)

            if request.method == "POST":
                form = CompleteOrderForm(request.POST or None, instance=order)
                total_price = 0
                for item in order_products:
                    item.save()
                    pre_product = PreparedProduct.objects.get(prepared_products_p_d=prepared_products_per_day, product=item.product)
                    pre_product.qty = pre_product.qty - item.qty
                    pre_product.sale_qty = pre_product.sale_qty + item.qty
                    pre_product.save()
                    order_product = item.qty * item.product.price
                    total_price += order_product
                if form.is_valid():
                    order = form.save(commit=False)
                    if form.cleaned_data['buying_type'] == 'simple':
                        order.status = 'completed'

                    if form.cleaned_data['buying_type'] == 'realization':
                        order.pay = 'kaspi'

                    if form.cleaned_data['pay'] == 'cash':
                        order.paid = True
                    order.finish_making = True
                    order.total_price = total_price
                    order.save()
                    return redirect('shop_detail', shop.id)
            else:
                form = CompleteOrderForm(request.POST or None, instance=order)

            context = {
                'order_products': order_products,
                'form': form,
                'order': order,
                'shop': shop
            }
            return render(request, 'delivery/order_complete.html', context)
        elif request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            deliveryman = Deliveryman.objects.get(user=request.user)
            shop = ShopBuyer.objects.get(id=kwargs.get('id'), deliveryman=deliveryman)
            order = Order.objects.get(user=request.user,
                                      role='deliveryman',
                                      buyer_shop=shop,
                                      finish_making=False,
                                      created_at=datetime.date.today())

            order_products = OrderProduct.objects.filter(order=order)
            prepared_products_per_day = PreparedProductsPerDay.objects.get(created_at=datetime.date.today())
            prepared_products = PreparedProduct.objects.filter(prepared_products_p_d=prepared_products_per_day)

            if request.method == "POST":
                form = CompleteOrderForm(request.POST or None, instance=order)
                total_price = 0
                for item in order_products:
                    item.save()
                    pre_product = PreparedProduct.objects.get(prepared_products_p_d=prepared_products_per_day, product=item.product)
                    pre_product.qty = pre_product.qty - item.qty
                    pre_product.sale_qty = pre_product.sale_qty + item.qty
                    pre_product.save()
                    order_product = item.qty * item.product.price
                    total_price += order_product
                if form.is_valid():
                    order = form.save(commit=False)
                    if form.cleaned_data['buying_type'] == 'simple':
                        order.status = 'completed'

                    if form.cleaned_data['buying_type'] == 'realization':
                        order.pay = 'kaspi'

                    if form.cleaned_data['pay'] == 'cash':
                        order.paid = True
                    order.finish_making = True
                    order.total_price = total_price
                    order.save()
                    return redirect('shop_detail', shop.id)
            else:
                form = CompleteOrderForm(request.POST or None, instance=order)

            context = {
                'order_products': order_products,
                'form': form,
                'order': order,
                'shop': shop
            }
            return render(request, 'delivery/order_complete.html', context)
        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")
        else:
            return redirect("/delivery/login")


class AddProductToOrder(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            product = Product.objects.get(id=kwargs.get('id'))
            order = Order.objects.get(id=kwargs.get('order_id'))
            prepared_products_per_day = PreparedProductsPerDay.objects.get(created_at=datetime.date.today())
            prepared_products = PreparedProduct.objects.filter(prepared_products_p_d=prepared_products_per_day)
            if PreparedProduct.objects.filter(prepared_products_p_d=prepared_products_per_day, product=product):
                if not OrderProduct.objects.filter(order=order, product=product):
                    OrderProduct.objects.create(order=order, product=product)
            id = kwargs.get('shop_id')
            return redirect("make_order", id)

        elif request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            product = Product.objects.get(id=kwargs.get('id'))
            order = Order.objects.get(id=kwargs.get('order_id'))
            prepared_products_per_day = PreparedProductsPerDay.objects.get(created_at=datetime.date.today())
            prepared_products = PreparedProduct.objects.filter(prepared_products_p_d=prepared_products_per_day)
            if PreparedProduct.objects.filter(prepared_products_p_d=prepared_products_per_day, product=product):
                if not OrderProduct.objects.filter(order=order, product=product):
                    OrderProduct.objects.create(order=order, product=product)
            id = kwargs.get('shop_id')
            return redirect("make_order", id)
        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")
        else:
            return redirect("/delivery/login")


class DeleteProductToOrder(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            product = Product.objects.get(id=kwargs.get('id'))
            order = Order.objects.get(id=kwargs.get('order_id'))
            OrderProduct.objects.get(order=order, product=product).delete()
            id = kwargs.get('shop_id')
            return redirect("make_order", id)
        elif request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            product = Product.objects.get(id=kwargs.get('id'))
            order = Order.objects.get(id=kwargs.get('order_id'))
            OrderProduct.objects.get(order=order, product=product).delete()
            id = kwargs.get('shop_id')
            return redirect("make_order", id)
        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")
        else:
            return redirect("/delivery/login")


class ChangeQtyOrder(View):

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            qty = int(request.POST.get('qty'))
            OrderProduct.objects.filter(id=kwargs.get('id')).update(qty=qty)
            id = kwargs.get('shop_id')
            return redirect("make_order", id)
        elif request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            qty = int(request.POST.get('qty'))
            OrderProduct.objects.filter(id=kwargs.get('id')).update(qty=qty)
            id = kwargs.get('shop_id')
            return redirect("make_order", id)
        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")
        else:
            return redirect("/delivery/login")

#Возвраты
class ShopRefundsDetailView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            shop = ShopBuyer.objects.get(id=kwargs.get('id'))
            refunds = Refund.objects.filter(buyer_shop=shop, finish_making=True).order_by('-id')
            refund_products = RefundProduct.objects.filter(refund__in=refunds).order_by('-id')

            context = {
                'refund_products': refund_products,
                'refunds': refunds,
                'shop': shop
            }
            return render(request, 'delivery/shop_refunds_detail.html', context)
        elif request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            deliveryman = Deliveryman.objects.get(user=request.user)
            shop = ShopBuyer.objects.get(id=kwargs.get('id'), deliveryman=deliveryman)
            refunds = Refund.objects.filter(buyer_shop=shop, finish_making=True).order_by('-id')
            refund_products = RefundProduct.objects.filter(refund__in=refunds).order_by('-id')

            context = {
                'refund_products': refund_products,
                'refunds': refunds,
                'shop': shop
            }
            return render(request, 'delivery/shop_refunds_detail.html', context)
        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")
        else:
            return redirect("/delivery/login")


class MakeRefundChoiceView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            shop = ShopBuyer.objects.get(id=kwargs.get('id'))
            prepared_products_per_day = PreparedProductsPerDay.objects.get(created_at=datetime.date.today())
            prepared_products = PreparedProduct.objects.filter(prepared_products_p_d=prepared_products_per_day)
            categories = Category.objects.all()
            products = Product.objects.all()

            if not Refund.objects.filter(user=request.user, buyer_shop=shop, finish_making=False, created_at=datetime.date.today()):
                refund = Refund.objects.create(
                                            user=request.user,
                                            buyer_shop=shop
                                            )
            else:
                refund = Refund.objects.get(
                                            user=request.user,
                                            buyer_shop=shop,
                                            finish_making=False,
                                            created_at=datetime.date.today()
                                            )
            refund_products = RefundProduct.objects.filter(refund=refund)
            context = {
                'refund': refund,
                'categories': categories,
                'prepared_products': prepared_products,
                'refund_products': refund_products,
                'products': products,
                'shop': shop
            }
            return render(request, 'delivery/refund_choice.html', context)
        elif request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            deliveryman = Deliveryman.objects.get(user=request.user)
            shop = ShopBuyer.objects.get(id=kwargs.get('id'), deliveryman=deliveryman)
            prepared_products_per_day = PreparedProductsPerDay.objects.get(created_at=datetime.date.today())
            prepared_products = PreparedProduct.objects.filter(prepared_products_p_d=prepared_products_per_day)
            categories = Category.objects.all()
            products = Product.objects.all()

            if not Refund.objects.filter(user=request.user, buyer_shop=shop, finish_making=False, created_at=datetime.date.today()):
                refund = Refund.objects.create(
                                            user=request.user,
                                            buyer_shop=shop
                                            )
            else:
                refund = Refund.objects.get(
                                            user=request.user,
                                            buyer_shop=shop,
                                            finish_making=False,
                                            created_at=datetime.date.today()
                                            )
            refund_products = RefundProduct.objects.filter(refund=refund)
            context = {
                'refund': refund,
                'categories': categories,
                'prepared_products': prepared_products,
                'refund_products': refund_products,
                'products': products,
                'shop': shop
            }
            return render(request, 'delivery/refund_choice.html', context)
        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")
        else:
            return redirect("/delivery/login")


class CompleteRefundView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            shop = ShopBuyer.objects.get(id=kwargs.get('id'))
            refund = Refund.objects.get(
                                        user=request.user,
                                        buyer_shop=shop,
                                        finish_making=False,
                                        created_at=datetime.date.today()
                                        )
            form = CompleteRefundForm(request.POST or None, instance=refund)
            refund_products = RefundProduct.objects.filter(refund=refund)
            total_price = 0
            for item in refund_products:
                refund_product = item.qty * item.product.price
                total_price += refund_product

            context = {
                'total_price': total_price,
                'refund_products': refund_products,
                'form': form,
                'refund': refund,
                'shop': shop
            }
            return render(request, 'delivery/refund_complete.html', context)
        elif request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            deliveryman = Deliveryman.objects.get(user=request.user)
            shop = ShopBuyer.objects.get(id=kwargs.get('id'), deliveryman=deliveryman)
            refund = Refund.objects.get(
                                        user=request.user,
                                        buyer_shop=shop,
                                        finish_making=False,
                                        created_at=datetime.date.today()
                                        )
            form = CompleteRefundForm(request.POST or None, instance=refund)
            refund_products = RefundProduct.objects.filter(refund=refund)
            total_price = 0
            for item in refund_products:
                refund_product = item.qty * item.product.price
                total_price += refund_product

            context = {
                'total_price': total_price,
                'refund_products': refund_products,
                'form': form,
                'refund': refund,
                'shop': shop
            }
            return render(request, 'delivery/refund_complete.html', context)
        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")
        else:
            return redirect("/delivery/login")

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            shop = ShopBuyer.objects.get(id=kwargs.get('id'))
            refund = Refund.objects.get(
                                        user=request.user,
                                        buyer_shop=shop,
                                        finish_making=False,
                                        created_at=datetime.date.today())

            refund_products = RefundProduct.objects.filter(refund=refund)
            prepared_products_per_day = PreparedProductsPerDay.objects.get(created_at=datetime.date.today())
            prepared_products = PreparedProduct.objects.filter(prepared_products_p_d=prepared_products_per_day)

            if request.method == "POST":
                form = CompleteRefundForm(request.POST or None, instance=refund)
                total_price = 0
                for item in refund_products:
                    item.save()
                    refund_product = item.qty * item.product.price
                    total_price += refund_product

                for item in refund_products:
                    pre_product = PreparedProduct.objects.get(prepared_products_p_d=prepared_products_per_day, product=item.product)
                    pre_product.qty = pre_product.qty - item.qty
                    pre_product.refund_qty = pre_product.refund_qty + item.qty
                    pre_product.save()

                if form.is_valid():
                    refund = form.save(commit=False)
                    refund.finish_making = True
                    refund.total_price = total_price
                    refund.save()
                    return redirect('shop_detail', shop.id)
            else:
                form = CompleteRefundForm(request.POST or None, instance=refund)

            context = {
                'refund_products': refund_products,
                'form': form,
                'refund': refund,
                'shop': shop
            }
            return render(request, 'delivery/refund_complete.html', context)

        elif request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            deliveryman = Deliveryman.objects.get(user=request.user)
            shop = ShopBuyer.objects.get(id=kwargs.get('id'), deliveryman=deliveryman)
            refund = Refund.objects.get(
                                        user=request.user,
                                        buyer_shop=shop,
                                        finish_making=False,
                                        created_at=datetime.date.today())

            refund_products = RefundProduct.objects.filter(refund=refund)
            prepared_products_per_day = PreparedProductsPerDay.objects.get(created_at=datetime.date.today())
            prepared_products = PreparedProduct.objects.filter(prepared_products_p_d=prepared_products_per_day)

            if request.method == "POST":
                form = CompleteRefundForm(request.POST or None, instance=refund)
                total_price = 0
                for item in refund_products:
                    item.save()
                    refund_product = item.qty * item.product.price
                    total_price += refund_product

                for item in refund_products:
                    pre_product = PreparedProduct.objects.get(prepared_products_p_d=prepared_products_per_day, product=item.product)
                    pre_product.qty = pre_product.qty - item.qty
                    pre_product.refund_qty = pre_product.refund_qty + item.qty
                    pre_product.save()

                if form.is_valid():
                    refund = form.save(commit=False)
                    refund.finish_making = True
                    refund.total_price = total_price
                    refund.save()
                    return redirect('shop_detail', shop.id)
            else:
                form = CompleteRefundForm(request.POST or None, instance=refund)

            context = {
                'refund_products': refund_products,
                'form': form,
                'refund': refund,
                'shop': shop
            }
            return render(request, 'delivery/refund_complete.html', context)
        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")
        else:
            return redirect("/delivery/login")


class AddProductToRefund(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            product = Product.objects.get(id=kwargs.get('id'))
            refund = Refund.objects.get(id=kwargs.get('refund_id'))
            prepared_products_per_day = PreparedProductsPerDay.objects.get(created_at=datetime.date.today())
            prepared_products = PreparedProduct.objects.filter(prepared_products_p_d=prepared_products_per_day)
            if PreparedProduct.objects.filter(prepared_products_p_d=prepared_products_per_day, product=product):
                if not RefundProduct.objects.filter(refund=refund, product=product):
                    RefundProduct.objects.create(refund=refund, product=product)
            id = kwargs.get('shop_id')
            return redirect("make_refund", id)
        elif request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            product = Product.objects.get(id=kwargs.get('id'))
            refund = Refund.objects.get(id=kwargs.get('refund_id'))
            prepared_products_per_day = PreparedProductsPerDay.objects.get(created_at=datetime.date.today())
            prepared_products = PreparedProduct.objects.filter(prepared_products_p_d=prepared_products_per_day)
            if PreparedProduct.objects.filter(prepared_products_p_d=prepared_products_per_day, product=product):
                if not RefundProduct.objects.filter(refund=refund, product=product):
                    RefundProduct.objects.create(refund=refund, product=product)
            id = kwargs.get('shop_id')
            return redirect("make_refund", id)
        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")
        else:
            return redirect("/delivery/login")


class DeleteProductToRefund(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            product = Product.objects.get(id=kwargs.get('id'))
            refund = Refund.objects.get(id=kwargs.get('refund_id'))
            RefundProduct.objects.get(refund=refund, product=product).delete()
            id = kwargs.get('shop_id')
            return redirect("make_refund", id)
        elif request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            product = Product.objects.get(id=kwargs.get('id'))
            refund = Refund.objects.get(id=kwargs.get('refund_id'))
            RefundProduct.objects.get(refund=refund, product=product).delete()
            id = kwargs.get('shop_id')
            return redirect("make_refund", id)
        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")
        else:
            return redirect("/delivery/login")


class ChangeQtyRefund(View):

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            qty = int(request.POST.get('qty'))
            RefundProduct.objects.filter(id=kwargs.get('id')).update(qty=qty)
            id = kwargs.get('shop_id')
            return redirect("make_refund", id)
        elif request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            qty = int(request.POST.get('qty'))
            RefundProduct.objects.filter(id=kwargs.get('id')).update(qty=qty)
            id = kwargs.get('shop_id')
            return redirect("make_refund", id)
        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")
        else:
            return redirect("/delivery/login")


#Акции
class ShopStocksDetailView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            shop = ShopBuyer.objects.get(id=kwargs.get('id'))
            stocks = Stocks.objects.filter(buyer_shop=shop, finish_making=True).order_by('-id')
            stock_products = StocksProduct.objects.filter(stocks__in=stocks).order_by('-id')

            context = {
                'stock_products': stock_products,
                'stocks': stocks,
                'shop': shop
            }
            return render(request, 'delivery/shop_stocks_detail.html', context)
        elif request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            deliveryman = Deliveryman.objects.get(user=request.user)
            shop = ShopBuyer.objects.get(id=kwargs.get('id'), deliveryman=deliveryman)
            stocks = Stocks.objects.filter(buyer_shop=shop, finish_making=True).order_by('-id')
            stock_products = StocksProduct.objects.filter(stocks__in=stocks).order_by('-id')

            context = {
                'stock_products': stock_products,
                'stocks': stocks,
                'shop': shop
            }
            return render(request, 'delivery/shop_stocks_detail.html', context)
        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")
        else:
            return redirect("/delivery/login")


class CompleteStocksView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            shop = ShopBuyer.objects.get(id=kwargs.get('id'))
            stocks = Stocks.objects.get(
                                        user=request.user,
                                        buyer_shop=shop,
                                        finish_making=False,
                                        created_at=datetime.date.today())
            form = CompleteStocksForm(request.POST or None, instance=stocks)
            stock_products = StocksProduct.objects.filter(stocks=stocks)
            total_price = 0
            for item in stock_products:
                stock_product = item.qty * item.product.price
                total_price += stock_product

            context = {
                'total_price': total_price,
                'stock_products': stock_products,
                'form': form,
                'stocks': stocks,
                'shop': shop
            }
            return render(request, 'delivery/stocks_complete.html', context)
        elif request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            deliveryman = Deliveryman.objects.get(user=request.user)
            shop = ShopBuyer.objects.get(id=kwargs.get('id'), deliveryman=deliveryman)
            stocks = Stocks.objects.get(
                                        user=request.user,
                                        buyer_shop=shop,
                                        finish_making=False,
                                        created_at=datetime.date.today())
            form = CompleteStocksForm(request.POST or None, instance=stocks)
            stock_products = StocksProduct.objects.filter(stocks=stocks)
            total_price = 0
            for item in stock_products:
                stock_product = item.qty * item.product.price
                total_price += stock_product

            context = {
                'total_price': total_price,
                'stock_products': stock_products,
                'form': form,
                'stocks': stocks,
                'shop': shop
            }
            return render(request, 'delivery/stocks_complete.html', context)
        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")
        else:
            return redirect("/delivery/login")

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            shop = ShopBuyer.objects.get(id=kwargs.get('id'))
            stocks = Stocks.objects.get(
                                        user=request.user,
                                        buyer_shop=shop,
                                        finish_making=False,
                                        created_at=datetime.date.today())

            stock_products = StocksProduct.objects.filter(stocks=stocks)
            prepared_products_per_day = PreparedProductsPerDay.objects.get(created_at=datetime.date.today())
            prepared_products = PreparedProduct.objects.filter(prepared_products_p_d=prepared_products_per_day)

            if request.method == "POST":
                form = CompleteStocksForm(request.POST or None, instance=stocks)
                total_price = 0
                for item in stock_products:
                    item.save()
                    stock_product = item.qty * item.product.price
                    total_price += stock_product

                for item in stock_products:
                    pre_product = PreparedProduct.objects.get(prepared_products_p_d=prepared_products_per_day, product=item.product)
                    pre_product.qty = pre_product.qty - item.qty
                    pre_product.stocks_qty = pre_product.stocks_qty + item.qty
                    pre_product.save()

                if form.is_valid():
                    stock = form.save(commit=False)
                    stock.finish_making = True
                    stock.total_price = total_price
                    stock.save()
                    return redirect('shop_detail', shop.id)
            else:
                form = CompleteStocksForm(request.POST or None, instance=stocks)

            context = {
                'stock_products': stock_products,
                'form': form,
                'stocks': stocks,
                'shop': shop
            }
            return render(request, 'delivery/stocks_complete.html', context)
        elif request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            deliveryman = Deliveryman.objects.get(user=request.user)
            shop = ShopBuyer.objects.get(id=kwargs.get('id'), deliveryman=deliveryman)
            stocks = Stocks.objects.get(
                                        user=request.user,
                                        buyer_shop=shop,
                                        finish_making=False,
                                        created_at=datetime.date.today())

            stock_products = StocksProduct.objects.filter(stocks=stocks)
            prepared_products_per_day = PreparedProductsPerDay.objects.get(created_at=datetime.date.today())
            prepared_products = PreparedProduct.objects.filter(prepared_products_p_d=prepared_products_per_day)

            if request.method == "POST":
                form = CompleteStocksForm(request.POST or None, instance=stocks)
                total_price = 0
                for item in stock_products:
                    item.save()
                    stock_product = item.qty * item.product.price
                    total_price += stock_product

                for item in stock_products:
                    pre_product = PreparedProduct.objects.get(prepared_products_p_d=prepared_products_per_day, product=item.product)
                    pre_product.qty = pre_product.qty - item.qty
                    pre_product.stocks_qty = pre_product.stocks_qty + item.qty
                    pre_product.save()

                if form.is_valid():
                    stock = form.save(commit=False)
                    stock.finish_making = True
                    stock.total_price = total_price
                    stock.save()
                    return redirect('shop_detail', shop.id)
            else:
                form = CompleteStocksForm(request.POST or None, instance=stocks)

            context = {
                'stock_products': stock_products,
                'form': form,
                'stocks': stocks,
                'shop': shop
            }
            return render(request, 'delivery/stocks_complete.html', context)
        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")
        else:
            return redirect("/delivery/login")


class MakeStocksChoiceView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            shop = ShopBuyer.objects.get(id=kwargs.get('id'))
            prepared_products_per_day = PreparedProductsPerDay.objects.get(created_at=datetime.date.today())
            prepared_products = PreparedProduct.objects.filter(prepared_products_p_d=prepared_products_per_day)
            categories = Category.objects.all()
            products = Product.objects.all()

            if not Stocks.objects.filter(user=request.user, buyer_shop=shop, finish_making=False, created_at=datetime.date.today()):
                stocks = Stocks.objects.create(
                                            user=request.user,
                                            buyer_shop=shop
                                            )
            else:
                stocks = Stocks.objects.get(
                                            user=request.user,
                                            buyer_shop=shop,
                                            finish_making=False,
                                            created_at=datetime.date.today()
                                            )
            stock_products = StocksProduct.objects.filter(stocks=stocks)
            context = {
                'stocks': stocks,
                'categories': categories,
                'prepared_products': prepared_products,
                'stock_products': stock_products,
                'products': products,
                'shop': shop
            }
            return render(request, 'delivery/stocks_choice.html', context)

        elif request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            deliveryman = Deliveryman.objects.get(user=request.user)
            shop = ShopBuyer.objects.get(id=kwargs.get('id'), deliveryman=deliveryman)
            prepared_products_per_day = PreparedProductsPerDay.objects.get(created_at=datetime.date.today())
            prepared_products = PreparedProduct.objects.filter(prepared_products_p_d=prepared_products_per_day)
            categories = Category.objects.all()
            products = Product.objects.all()

            if not Stocks.objects.filter(user=request.user, buyer_shop=shop, finish_making=False, created_at=datetime.date.today()):
                stocks = Stocks.objects.create(
                                            user=request.user,
                                            buyer_shop=shop
                                            )
            else:
                stocks = Stocks.objects.get(
                                            user=request.user,
                                            buyer_shop=shop,
                                            finish_making=False,
                                            created_at=datetime.date.today()
                                            )
            stock_products = StocksProduct.objects.filter(stocks=stocks)
            context = {
                'stocks': stocks,
                'categories': categories,
                'prepared_products': prepared_products,
                'stock_products': stock_products,
                'products': products,
                'shop': shop
            }
            return render(request, 'delivery/stocks_choice.html', context)
        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")
        else:
            return redirect("/delivery/login")


class AddProductToStocks(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            product = Product.objects.get(id=kwargs.get('id'))
            stocks = Stocks.objects.get(id=kwargs.get('stocks_id'))
            prepared_products_per_day = PreparedProductsPerDay.objects.get(created_at=datetime.date.today())
            prepared_products = PreparedProduct.objects.filter(prepared_products_p_d=prepared_products_per_day)
            if PreparedProduct.objects.filter(prepared_products_p_d=prepared_products_per_day, product=product):
                if not StocksProduct.objects.filter(stocks=stocks, product=product):
                    StocksProduct.objects.create(stocks=stocks, product=product)
            id = kwargs.get('shop_id')
            return redirect("make_stocks", id)
        elif request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            product = Product.objects.get(id=kwargs.get('id'))
            stocks = Stocks.objects.get(id=kwargs.get('stocks_id'))
            prepared_products_per_day = PreparedProductsPerDay.objects.get(created_at=datetime.date.today())
            prepared_products = PreparedProduct.objects.filter(prepared_products_p_d=prepared_products_per_day)
            if PreparedProduct.objects.filter(prepared_products_p_d=prepared_products_per_day, product=product):
                if not StocksProduct.objects.filter(stocks=stocks, product=product):
                    StocksProduct.objects.create(stocks=stocks, product=product)
            id = kwargs.get('shop_id')
            return redirect("make_stocks", id)
        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")
        else:
            return redirect("/delivery/login")


class DeleteProductToStocks(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            product = Product.objects.get(id=kwargs.get('id'))
            stocks = Stocks.objects.get(id=kwargs.get('stocks_id'))
            StocksProduct.objects.get(stocks=stocks, product=product).delete()
            id = kwargs.get('shop_id')
            return redirect("make_stocks", id)
        elif request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            product = Product.objects.get(id=kwargs.get('id'))
            stocks = Stocks.objects.get(id=kwargs.get('stocks_id'))
            StocksProduct.objects.get(stocks=stocks, product=product).delete()
            id = kwargs.get('shop_id')
            return redirect("make_stocks", id)
        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")
        else:
            return redirect("/delivery/login")


class ChangeQtyStocks(View):

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            qty = int(request.POST.get('qty'))
            StocksProduct.objects.filter(id=kwargs.get('id')).update(qty=qty)
            id = kwargs.get('shop_id')
            return redirect("make_stocks", id)
        elif request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            qty = int(request.POST.get('qty'))
            StocksProduct.objects.filter(id=kwargs.get('id')).update(qty=qty)
            id = kwargs.get('shop_id')
            return redirect("make_stocks", id)
        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")
        else:
            return redirect("/delivery/login")

#Создание магазина
class NewShopView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            deliveryman = Deliveryman.objects.get(user=request.user)
            form = NewShopForm(request.POST or None)
            # shop_admin = ShopAdministrator.objects.get(id=kwargs.get('id'))
            context = {
                'form': form,
            }
            return render(request, 'delivery/new_shop.html', context)
        elif request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            deliveryman = Deliveryman.objects.get(user=request.user)
            form = NewShopForm(request.POST or None)
            # shop_admin = ShopAdministrator.objects.get(id=kwargs.get('id'))
            context = {
                'form': form,
            }
            return render(request, 'delivery/new_shop.html', context)
        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")
        else:
            return redirect("/delivery/login")

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            deliveryman = Deliveryman.objects.get(user=request.user)
            # shop_admin = ShopAdministrator.objects.get(id=kwargs.get('id'))
            # shop_admin = ShopAdministrator.objects.get(id=1)
            if request.method == "POST":
                form = NewShopForm(request.POST or None)

                if form.is_valid():
                    shop = form.save(commit=False)
                    shop.deliveryman = deliveryman
                    # shop.customer = shop_admin
                    shop.save()
                    return redirect('delivery_base')
            else:
                form = NewShopForm(request.POST or None)

            context = {
                'form': form,
            }
            return render(request, 'delivery/new_shop.html', context)

        elif request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            deliveryman = Deliveryman.objects.get(user=request.user)
            # shop_admin = ShopAdministrator.objects.get(id=kwargs.get('id'))
            # shop_admin = ShopAdministrator.objects.get(id=1)
            if request.method == "POST":
                form = NewShopForm(request.POST or None)

                if form.is_valid():
                    shop = form.save(commit=False)
                    shop.deliveryman = deliveryman
                    # shop.customer = shop_admin
                    shop.save()
                    return redirect('delivery_base')
            else:
                form = NewShopForm(request.POST or None)

            context = {
                'form': form,
            }
            return render(request, 'delivery/new_shop.html', context)
        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")
        else:
            return redirect("/delivery/login")


class NewShopAdminView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            deliveryman = Deliveryman.objects.get(user=request.user)
            form = RegistrationForm(request.POST or None)
            form_2 = NewShopAdminForm(request.POST or None)
            context = {
                'form': form,
                'form_2': form_2
            }
            return render(request, 'delivery/new_shop_admin.html', context)
        elif request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            deliveryman = Deliveryman.objects.get(user=request.user)
            form = RegistrationForm(request.POST or None)
            form_2 = NewShopAdminForm(request.POST or None)
            context = {
                'form': form,
                'form_2': form_2
            }
            return render(request, 'delivery/new_shop_admin.html', context)
        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")
        else:
            return redirect("/delivery/login")

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            deliveryman = Deliveryman.objects.get(user=request.user)

            if request.method == "POST":
                form = RegistrationForm(request.POST or None)
                form_2 = NewShopAdminForm(request.POST or None)

                if form.is_valid():
                    user = form.save(commit=False)
                    user.save()

                    if form_2.is_valid():
                        form_2 = form_2.save(commit=False)
                        form_2.user = user
                        form_2.first_name = form.cleaned_data['first_name']
                        form_2.email = form.cleaned_data['email']
                        form_2.save()
                        return redirect('new_shop', form_2.id)
            else:
                form = NewShopForm(request.POST or None)

            context = {
                'form': form,
                'form_2': form_2
            }
            return render(request, 'delivery/new_shop_admin.html', context)
        elif request.user.is_authenticated == True and Deliveryman.objects.filter(user=request.user):
            deliveryman = Deliveryman.objects.get(user=request.user)

            if request.method == "POST":
                form = RegistrationForm(request.POST or None)
                form_2 = NewShopAdminForm(request.POST or None)

                if form.is_valid():
                    user = form.save(commit=False)
                    user.save()

                    if form_2.is_valid():
                        form_2 = form_2.save(commit=False)
                        form_2.user = user
                        form_2.first_name = form.cleaned_data['first_name']
                        form_2.email = form.cleaned_data['email']
                        form_2.save()
                        return redirect('new_shop', form_2.id)
            else:
                form = NewShopForm(request.POST or None)

            context = {
                'form': form,
                'form_2': form_2
            }
            return render(request, 'delivery/new_shop_admin.html', context)
        elif request.user.is_authenticated == True and not Deliveryman.objects.filter(user=request.user):
            return redirect("/")
        else:
            return redirect("/delivery/login")
