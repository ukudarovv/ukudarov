from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, get_user_model
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import DetailView, View, TemplateView
from django.contrib.auth.models import Group
from django.shortcuts import get_list_or_404, get_object_or_404, render
from datetime import datetime, timedelta, date
from django.forms import inlineformset_factory, modelformset_factory
from siteadmin.num2t4ru import num2text

from django.template.loader import get_template, render_to_string
from weasyprint import HTML
import tempfile

from products.models import *
from users.models import *
from carts.models import *
from orders.models import *
from shop_statistics.models import *
from menu.models import *

from .forms import *


class AdminBaseView(View):

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated == True and request.user.is_staff == True:
            if not PreparedProductsPerDay.objects.filter(created_at=datetime.now()):
                prepared_products_per_day = PreparedProductsPerDay.objects.create()
            else:
                prepared_products_per_day = PreparedProductsPerDay.objects.get(created_at=datetime.now())
            prepared_products = PreparedProduct.objects.filter(prepared_products_p_d=prepared_products_per_day)

            realization_orders = Order.objects.filter(finish_making=True, created_at=datetime.now(), buying_type='realization').order_by('-id')
            realization_order_products = OrderProduct.objects.filter(order__in=realization_orders).order_by('-id')

            orders = Order.objects.filter(finish_making=True, created_at=datetime.now(), buying_type='simple').order_by('-id')
            order_products = OrderProduct.objects.filter(order__in=orders).order_by('-id')

            orders_kaspi = Order.objects.filter(finish_making=True, created_at=datetime.now(), buying_type='simple', pay='kaspi').order_by('-id')
            orders_cash = Order.objects.filter(finish_making=True, created_at=datetime.now(), buying_type='simple', pay='cash').order_by('-id')

            refunds = Refund.objects.filter(finish_making=True, created_at=datetime.now()).order_by('-id')
            refund_products = RefundProduct.objects.filter(refund__in=refunds).order_by('-id')
            stocks = Stocks.objects.filter(finish_making=True, created_at=datetime.now()).order_by('-id')
            stock_products = StocksProduct.objects.filter(stocks__in=stocks).order_by('-id')

            if not ForDay.objects.filter(created_at=datetime.now()):
                for_day = ForDay.objects.create()

                order_sum = 0
                order_debt = 0
                order_qty = 0

                order_sum_kaspi = 0
                order_debt_kaspi = 0

                order_sum_cash = 0
                order_debt_cash = 0

                order_sum_r = 0
                order_realization_debt = 0
                order_qty_r = 0

                refund_sum = 0
                refund_qty = 0
                stocks_sum = 0
                stocks_qty = 0

                for item in orders:
                    if item.paid == True:
                        order_sum = order_sum + item.total_price
                    elif item.paid == False:
                        order_debt = order_debt + item.total_price
                    order_qty = order_qty + 1

                for item in orders_kaspi:
                    if item.paid == True:
                        order_sum_kaspi = order_sum_kaspi + item.total_price
                    elif item.paid == False:
                        order_debt_kaspi = order_debt_kaspi + item.total_price

                for item in orders_cash:
                    if item.paid == True:
                        order_sum_cash = order_sum_cash + item.total_price
                    elif item.paid == False:
                        order_debt_cash = order_debt_cash + item.total_price

                for item in realization_orders:
                    if item.paid == True:
                        order_sum_r = order_sum_r + item.total_price
                    elif item.paid == False:
                        order_realization_debt = order_realization_debt + item.total_price
                    order_qty_r = order_qty_r + 1

                for item in refunds:
                    refund_sum = refund_sum + item.total_price
                    refund_qty = refund_qty + 1

                for item in stocks:
                    stocks_sum = stocks_sum + item.total_price
                    stocks_qty = stocks_qty + 1

                for_day.order_cash = order_sum_cash
                for_day.order_kaspi = order_sum_kaspi

                for_day.order_debt_cash = order_debt_cash
                for_day.order_debt_kaspi = order_debt_kaspi

                for_day.order = order_sum
                for_day.order_debt = order_debt
                for_day.order_qty = order_qty
                for_day.order_realization = order_sum_r
                for_day.order_realization_debt = order_realization_debt
                for_day.order_realization_qty = order_qty_r
                for_day.refund = refund_sum
                for_day.refund_qty = refund_qty
                for_day.stocks = stocks_sum
                for_day.stocks_qty = stocks_qty
                for_day.week_day = datetime.datetime.today().isoweekday()
                for_day.save()
            else:
                for_day = ForDay.objects.get(created_at=datetime.now())
                order_sum = 0
                order_debt = 0
                order_qty = 0

                order_sum_kaspi = 0
                order_debt_kaspi = 0

                order_sum_cash = 0
                order_debt_cash = 0

                order_sum_r = 0
                order_realization_debt = 0
                order_qty_r = 0

                refund_sum = 0
                refund_qty = 0
                stocks_sum = 0
                stocks_qty = 0

                for item in orders:
                    if item.paid == True:
                        order_sum = order_sum + item.total_price
                    elif item.paid == False:
                        order_debt = order_debt + item.total_price
                    order_qty = order_qty + 1

                for item in orders_kaspi:
                    if item.paid == True:
                        order_sum_kaspi = order_sum_kaspi + item.total_price
                    elif item.paid == False:
                        order_debt_kaspi = order_debt_kaspi + item.total_price

                for item in orders_cash:
                    if item.paid == True:
                        order_sum_cash = order_sum_cash + item.total_price
                    elif item.paid == False:
                        order_debt_cash = order_debt_cash + item.total_price

                for item in realization_orders:
                    if item.paid == True:
                        order_sum_r = order_sum_r + item.total_price
                    elif item.paid == False:
                        order_realization_debt = order_realization_debt + item.total_price
                    order_qty_r = order_qty_r + 1

                for item in refunds:
                    refund_sum = refund_sum + item.total_price
                    refund_qty = refund_qty + 1

                for item in stocks:
                    stocks_sum = stocks_sum + item.total_price
                    stocks_qty = stocks_qty + 1

                for_day.order_cash = order_sum_cash
                for_day.order_kaspi = order_sum_kaspi

                for_day.order_debt_cash = order_debt_cash
                for_day.order_debt_kaspi = order_debt_kaspi

                for_day.order = order_sum
                for_day.order_debt = order_debt
                for_day.order_qty = order_qty
                for_day.order_realization = order_sum_r
                for_day.order_realization_debt = order_realization_debt
                for_day.order_realization_qty = order_qty_r
                for_day.refund = refund_sum
                for_day.refund_qty = refund_qty
                for_day.stocks = stocks_sum
                for_day.stocks_qty = stocks_qty
                for_day.save()


            context = {
                'for_day': for_day,
                'prepared_products_per_day': prepared_products_per_day,
                'prepared_products': prepared_products,
                'order_products': order_products,
                'orders': orders,
                'realization_orders': realization_orders,
                'realization_order_products': realization_order_products,
                'refund_products': refund_products,
                'refunds': refunds,
                'stocks': stocks,
                'stock_products': stock_products
            }
            return render(request, 'siteadmin/base.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class PreProductsView(View):

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated == True and request.user.is_staff == True:
            presentday = datetime.now()
            tomorrow = presentday + timedelta(1)
            if not PreparedProductsPerDay.objects.filter(created_at=tomorrow):
                prepared_products_per_day = PreparedProductsPerDay.objects.create(created_at=tomorrow)
            else:
                prepared_products_per_day = PreparedProductsPerDay.objects.get(created_at=tomorrow)
            prepared_products = PreparedProduct.objects.filter(prepared_products_p_d=prepared_products_per_day)

            context = {
                'prepared_products_per_day': prepared_products_per_day,
                'prepared_products': prepared_products,
            }
            return render(request, 'siteadmin/pre_products.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class NextAddPreparedProductView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            presentday = datetime.now()
            tomorrow = presentday + timedelta(1)
            if not PreparedProductsPerDay.objects.filter(created_at=tomorrow):
                prepared_products_per_day = PreparedProductsPerDay.objects.create(created_at=tomorrow)
            else:
                prepared_products_per_day = PreparedProductsPerDay.objects.get(created_at=tomorrow)
            form = AddPreparedProductForm(request.POST or None)
            context = {
                'form': form,
                'prepared_products_per_day': prepared_products_per_day,
            }
            return render(request, 'siteadmin/next_add_pre_product.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            presentday = datetime.now()
            tomorrow = presentday + timedelta(1)
            prepared_products_per_day = PreparedProductsPerDay.objects.get(created_at=tomorrow)
            prepared_products = PreparedProduct.objects.filter(prepared_products_p_d=prepared_products_per_day)
            if request.method == "POST":
                form = AddPreparedProductForm(request.POST or None)
                if form.is_valid():
                    for item in prepared_products:
                        if form.cleaned_data['product'] == item.product and prepared_products_per_day == item.prepared_products_p_d:
                            item.delete()
                    product = form.save(commit=False)
                    product.prepared_products_p_d = prepared_products_per_day
                    product.qty = form.cleaned_data['prepared_qty']
                    product.save()
                    return redirect('next_prepared_products')
            else:
                form = AddPreparedProductForm(request.POST or None)

            context = {
                'form': form,
                'prepared_products_per_day': prepared_products_per_day,
            }
            return render(request, 'siteadmin/next_add_pre_product.html', context)

        elif request.user.is_authenticated == True and request.user.is_staff == False:
            ("/")
        else:
            ("/administrator/login")


class NextEditPreparedProductView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            presentday = datetime.now()
            tomorrow = presentday + timedelta(1)
            if not PreparedProductsPerDay.objects.filter(created_at=tomorrow):
                prepared_products_per_day = PreparedProductsPerDay.objects.create(created_at=tomorrow)
            else:
                prepared_products_per_day = PreparedProductsPerDay.objects.get(created_at=tomorrow)
            form = AddPreparedProductForm(request.POST or None)
            context = {
                'form': form,
                'prepared_products_per_day': prepared_products_per_day,
            }
            return render(request, 'siteadmin/next_add_pre_product.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            presentday = datetime.now()
            tomorrow = presentday + timedelta(1)
            prepared_products_per_day = PreparedProductsPerDay.objects.get(created_at=tomorrow)
            prepared_products = PreparedProduct.objects.filter(prepared_products_p_d=prepared_products_per_day)
            if request.method == "POST":
                form = AddPreparedProductForm(request.POST or None)
                if form.is_valid():
                    for item in prepared_products:
                        if form.cleaned_data['product'] == item.product and prepared_products_per_day == item.prepared_products_p_d:
                            item.delete()
                    product = form.save(commit=False)
                    product.prepared_products_p_d = prepared_products_per_day
                    product.qty = form.cleaned_data['prepared_qty']
                    product.save()
                    return redirect('next_prepared_products')
            else:
                form = AddPreparedProductForm(request.POST or None)

            context = {
                'form': form,
                'prepared_products_per_day': prepared_products_per_day,
            }
            return render(request, 'siteadmin/next_add_pre_product.html', context)

        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class OrdersDetailView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            orders = Order.objects.filter(finish_making=True, buying_type='simple').order_by('-id')
            order_products = OrderProduct.objects.filter(order__in=orders).order_by('-id')
            paginator = Paginator(orders, 15)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context = {
                'order_products': order_products,
                'page_obj': page_obj,
            }
            return render(request, 'siteadmin/orders_detail.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class ChangeStatusPay(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:

            if kwargs.get('status') == 0:
                order = Order.objects.filter(id=kwargs.get('id')).update(paid=False, status='in_progress')
            elif kwargs.get('status') == 1:
                order = Order.objects.filter(id=kwargs.get('id')).update(paid=True, status='completed')

            url = kwargs.get('url')
            return redirect(url)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class RealizationOrdersDetailView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            orders = Order.objects.filter(finish_making=True, buying_type='realization').order_by('-id')
            order_products = OrderProduct.objects.filter(order__in=orders).order_by('-id')
            paginator = Paginator(orders, 15)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context = {
                'order_products': order_products,
                'page_obj': page_obj,
            }
            return render(request, 'siteadmin/realization_orders_detail.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class RefundsDetailView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            refunds = Refund.objects.filter(finish_making=True).order_by('-id')
            refund_products = RefundProduct.objects.filter(refund__in=refunds).order_by('-id')

            context = {
                'refund_products': refund_products,
                'refunds': refunds,
            }
            return render(request, 'siteadmin/refunds_detail.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class StocksDetailView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            stocks = Stocks.objects.filter(finish_making=True).order_by('-id')
            stock_products = StocksProduct.objects.filter(stocks__in=stocks).order_by('-id')

            context = {
                'stock_products': stock_products,
                'stocks': stocks,
            }
            return render(request, 'siteadmin/stocks_detail.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class AddPreparedProductView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            if not PreparedProductsPerDay.objects.filter(created_at=datetime.now()):
                prepared_products_per_day = PreparedProductsPerDay.objects.create()
            else:
                prepared_products_per_day = PreparedProductsPerDay.objects.get(created_at=datetime.now())
            form = AddPreparedProductForm(request.POST or None)
            context = {
                'form': form,
                'prepared_products_per_day': prepared_products_per_day,
            }
            return render(request, 'siteadmin/add_pre_product.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            prepared_products_per_day = PreparedProductsPerDay.objects.get(created_at=datetime.now())
            prepared_products = PreparedProduct.objects.filter(prepared_products_p_d=prepared_products_per_day)
            if request.method == "POST":
                form = AddPreparedProductForm(request.POST or None)
                if form.is_valid():
                    for item in prepared_products:
                        if form.cleaned_data['product'] == item.product and prepared_products_per_day == item.prepared_products_p_d:
                            item.delete()
                    product = form.save(commit=False)
                    product.prepared_products_p_d = prepared_products_per_day
                    product.qty = form.cleaned_data['prepared_qty']
                    product.save()
                    return redirect('admin_base')
            else:
                form = AddPreparedProductForm(request.POST or None)

            context = {
                'form': form,
                'prepared_products_per_day': prepared_products_per_day,
            }
            return render(request, 'siteadmin/add_pre_product.html', context)

        elif request.user.is_authenticated == True and request.user.is_staff == False:
            ("/")
        else:
            return redirect("/administrator/login")


class EditPreparedProductView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            if not PreparedProductsPerDay.objects.filter(created_at=datetime.now()):
                prepared_products_per_day = PreparedProductsPerDay.objects.create()
            else:
                prepared_products_per_day = PreparedProductsPerDay.objects.get(created_at=datetime.now())
            form = EditPreparedProductForm(request.POST or None)
            context = {
                'form': form,
                'prepared_products_per_day': prepared_products_per_day,
            }
            return render(request, 'siteadmin/add_pre_product.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            prepared_products_per_day = PreparedProductsPerDay.objects.get(created_at=datetime.now())
            prepared_products = PreparedProduct.objects.filter(prepared_products_p_d=prepared_products_per_day)
            if request.method == "POST":
                form = EditPreparedProductForm(request.POST or None)
                if form.is_valid():
                    product = form.save(commit=False)
                    for item in prepared_products:
                        if form.cleaned_data['product'] == item.product and prepared_products_per_day == item.prepared_products_p_d:
                            if form.cleaned_data['action'] == 'plus':
                                item.qty = item.qty + form.cleaned_data['prepared_qty']
                            elif form.cleaned_data['action'] == 'minus':
                                item.qty = item.qty - form.cleaned_data['prepared_qty']
                            item.save()
                    return redirect('admin_base')
            else:
                form = AddPreparedProductForm(request.POST or None)

            context = {
                'form': form,
                'prepared_products_per_day': prepared_products_per_day,
            }
            return render(request, 'siteadmin/add_pre_product.html', context)

        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class AdminLoginView(View):

    def get(self, request, *args, **kwargs):
        form = AdminLoginForm(request.POST or None)
        context = {
            'form': form,
        }
        if request.user.is_staff == True:
            return redirect("admin_base")
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return render(request, 'siteadmin/login.html', context)


    def post(self, request, *args, **kwargs):
        form = AdminLoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.get(username=username)
            if user.is_staff == True:
                user = authenticate(
                    username=username, password=password
                )
                if user:
                    login(request, user)
                    return HttpResponseRedirect('/administrator')
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
        return render(request, 'siteadmin/login.html', context)


class ProductsView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            products = Product.objects.all()

            context = {
                'products': products
            }
            return render(request, 'siteadmin/products_detail.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class AddProductView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            form = ProductForm(request.POST or None)
            context = {
                'form': form,
            }
            return render(request, 'siteadmin/add_product.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            if request.method == "POST":
                form = ProductForm(request.POST or None)
                if form.is_valid():
                    product = form.save(commit=False)
                    product.image = request.FILES.get('image')
                    product.save()
                    return redirect('admin_products')
            else:
                form = ProductForm(request.POST or None)

            context = {
                'form': form,
            }
            return render(request, 'siteadmin/add_product.html', context)

        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class EditProductView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            product = Product.objects.get(id=kwargs.get('id'))
            form = ProductForm(request.POST or None, instance=product)
            context = {
                'product': product,
                'form': form,
            }
            return render(request, 'siteadmin/edit_product.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            product = Product.objects.get(id=kwargs.get('id'))
            if request.method == "POST":
                form = ProductForm(request.POST or None, instance=product)
                if form.is_valid():
                    product = form.save(commit=False)
                    if request.FILES.get('image'):
                        product.image = request.FILES.get('image')
                    product.save()
                    return redirect('admin_products')
            else:
                form = ProductForm(request.POST or None, instance=product)

            context = {
                'product': product,
                'form': form,
            }
            return render(request, 'siteadmin/edit_product.html', context)

        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class DeleteProductView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            product = Product.objects.get(id=kwargs.get('id')).delete()
            return redirect("admin_base")
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class CategoryView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            category = Category.objects.all()

            context = {
                'category': category
            }
            return render(request, 'siteadmin/category_detail.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class AddCategoryView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            form = CategoryForm(request.POST or None)
            context = {
                'form': form,
            }
            return render(request, 'siteadmin/add_category.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            if request.method == "POST":
                form = CategoryForm(request.POST or None)
                if form.is_valid():
                    form.save()
                    return redirect('admin_base')
            else:
                form = CategoryForm(request.POST or None)

            context = {
                'form': form,
            }
            return render(request, 'siteadmin/add_category.html', context)

        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class DeleteCategoryView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            category = Category.objects.get(id=kwargs.get('id')).delete()

            return redirect("admin_base")
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class DeliverymanView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            deliveryman = Deliveryman.objects.all()

            context = {
                'deliveryman': deliveryman
            }
            return render(request, 'siteadmin/deliveryman_detail.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class EditDeliverymanView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            deliveryman = Deliveryman.objects.get(id=kwargs.get('id'))
            form = EditDeliverymanForm(request.POST or None, instance=deliveryman)
            context = {
                'deliveryman': deliveryman,
                'form': form,
            }
            return render(request, 'siteadmin/edit_deliveryman_detail.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            deliveryman = Deliveryman.objects.get(id=kwargs.get('id'))
            if request.method == "POST":
                form = EditDeliverymanForm(request.POST or None, instance=deliveryman)
                if form.is_valid():
                    form.save()
                    return redirect('admin_deliveryman')
            else:
                form = EditDeliverymanForm(request.POST or None, instance=deliveryman)

            context = {
                'deliveryman': deliveryman,
                'form': form,
            }
            return render(request, 'siteadmin/edit_deliveryman_detail.html', context)

        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class AddDeliverymanView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            form = DeliverymanForm(request.POST or None)
            form_2 = RegistrationForm(request.POST or None)
            context = {
                'form': form,
                'form_2': form_2,
            }
            return render(request, 'siteadmin/add_deliveryman_detail.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            if request.method == "POST":
                form = DeliverymanForm(request.POST or None)
                form_2 = RegistrationForm(request.POST or None)
                if form_2.is_valid():
                    new_user = form_2.save(commit=False)
                    new_user.set_password(form_2.cleaned_data["password"])
                    new_user.save()
                if form.is_valid():
                    user = form.save(commit=False)
                    user.user = new_user
                    user.first_name = form_2.cleaned_data['first_name']
                    user.email = form_2.cleaned_data['email']
                    user.save()
                    return redirect('admin_deliveryman')
            else:
                form = DeliverymanForm(request.POST or None)
                form_2 = RegistrationForm(request.POST or None)

            context = {
                'form': form,
                'form_2': form_2,
            }
            return render(request, 'siteadmin/add_deliveryman_detail.html', context)

        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class ShopsView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            shops = ShopBuyer.objects.all()

            context = {
                'shops': shops
            }
            return render(request, 'siteadmin/shops_detail.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class ShopContactDetailView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            shop = ShopBuyer.objects.get(id=kwargs.get('id'))
            context = {
                'shop': shop
            }
            return render(request, 'siteadmin/shop_contact_detail.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class EditShopContactView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            shop = ShopBuyer.objects.get(id=kwargs.get('id'))
            form = EditShopContactForm(request.POST or None, instance=shop)
            context = {
                'form': form,
                'shop': shop
            }
            return render(request, 'siteadmin/edit_shop_contact.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            shop = ShopBuyer.objects.get(id=kwargs.get('id'))

            if request.method == "POST":
                form = EditShopContactForm(request.POST or None, instance=shop)
                if form.is_valid():
                    form.save()
                    return redirect('admin_shop_detail', shop.id)
            else:
                form = EditShopContactForm(request.POST or None, instance=shop)

            context = {
                'form': form,
                'shop': shop
            }
            return render(request, 'siteadmin/edit_shop_contact.html', context)

        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


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
            return render(request, 'siteadmin/edit_shop_admin_contact.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            shop = ShopBuyer.objects.get(id=kwargs.get('id'))
            shop_admin = ShopAdministrator.objects.get(id=shop.customer.id)


            if request.method == "POST":
                form = EditShopAdminContactForm(request.POST or None, instance=shop_admin)
                if form.is_valid():
                    form.save()
                    return redirect('admin_shop_detail', shop.id)
            else:
                form = EditShopAdminContactForm(request.POST or None, instance=shop_admin)

            context = {
                'form': form,
                'shop': shop
            }
            return render(request, 'siteadmin/edit_shop_admin_contact.html', context)

        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class ShopOrdersDetailView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            shop = ShopBuyer.objects.get(id=kwargs.get('id'))
            orders = Order.objects.filter(buyer_shop=shop, finish_making=True).order_by('-id')
            order_products = OrderProduct.objects.filter(order__in=orders).order_by('-id')
            if PaymentInvoice.objects.filter(shop=shop, finish_making=False):
                pay_inv = PaymentInvoice.objects.get(shop=shop, finish_making=False)
                pay_inv_order = OrdersPaymentInvoice.objects.filter(pay_invoice=pay_inv)
                pay_inv_order_count = pay_inv_order.count()
            else:
                pay_inv = None
                pay_inv_order = 0
                pay_inv_order_count = 0

            context = {
                'order_products': order_products,
                'orders': orders,
                'shop': shop,
                'pay_inv': pay_inv,
                'pay_inv_order': pay_inv_order,
                'pay_inv_order_count': pay_inv_order_count
            }
            return render(request, 'siteadmin/shop_orders_detail.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


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
            return render(request, 'siteadmin/shop_refunds_detail.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


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
            return render(request, 'siteadmin/shop_stocks_detail.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class NewShopView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            form = EditShopContactForm(request.POST or None)
            context = {
                'form': form,
            }
            return render(request, 'siteadmin/new_shop.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            deliveryman = Deliveryman.objects.get(user=request.user)
            if request.method == "POST":
                EditShopContactForm

                if form.is_valid():
                    form.save()
                    return redirect('admin_shops')
            else:
                form = EditShopContactForm(request.POST or None)

            context = {
                'form': form,
            }
            return render(request, 'siteadmin/new_shop.html', context)

        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class UsersDetailView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            users = Customer.objects.all()

            context = {
                'users': users
            }
            return render(request, 'siteadmin/users_detail.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class ShopAdminsDetailView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            users = ShopAdministrator.objects.all()
            shops = ShopBuyer.objects.all()

            context = {
                'shops': shops,
                'users': users
            }
            return render(request, 'siteadmin/shop_admins_detail.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class DeleteShopView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            ShopBuyer.objects.get(id=kwargs.get('id')).delete()

            return redirect("admin_shops")
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class DeleteDeliverymanView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            Deliveryman.objects.get(id=kwargs.get('id')).delete()

            return redirect("admin_deliveryman")
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class InvoiceView(View):

    def get(self, request, *args, **kwargs):
        order = Order.objects.get(id=kwargs.get('id'))
        order.save()
        if Invoice.objects.filter(order=order):
            invoice = Invoice.objects.get(order=order)
        else:
            invoice = Invoice.objects.create(order=order, shop=order.buyer_shop, created_at=order.created_at)
        order_products = OrderProduct.objects.filter(order=order)
        total_qty = 0
        for item in order_products:
            total_qty = total_qty + item.qty
        order_total = num2text(order.total_price)
        order_total_qty = num2text(total_qty)

        context = {
            'total_qty': total_qty,
            'order_total_qty': order_total_qty,
            'order_total': order_total,
            'order_products': order_products,
            'order': order,
            'invoice': invoice,
        }
        return render(request, 'siteadmin/invoice_template.html', context)


class InvoicePDFView(View):

    def get(self, request, *args, **kwargs):
        order = Order.objects.get(id=kwargs.get('id'))
        order.save()
        if Invoice.objects.filter(order=order):
            invoice = Invoice.objects.get(order=order)
        else:
            invoice = Invoice.objects.create(order=order, shop=order.buyer_shop, created_at=order.created_at)
        order_products = OrderProduct.objects.filter(order=order)
        total_qty = 0
        for item in order_products:
            total_qty = total_qty + item.qty
        order_total = num2text(order.total_price)
        order_total_qty = num2text(total_qty)

        responce = HttpResponse(content_type='application/pdf')
        responce['Content-Disposition'] = 'inline; filename=Накладная' + \
            str(order.buyer_shop.title)+'.pdf'
        responce['Content-Transfer-Encoding'] = 'binary'

        context = {
            'total_qty': total_qty,
            'order_total_qty': order_total_qty,
            'order_total': order_total,
            'order_products': order_products,
            'order': order,
            'invoice': invoice,
        }

        html_string = render_to_string('siteadmin/invoice_template.html', context)
        html = HTML(string=html_string)

        result = html.write_pdf()

        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            responce.write(output.read())

        return responce


class Invoice2View(View):

    def get(self, request, *args, **kwargs):
        order = Order.objects.get(id=kwargs.get('id'))
        order.save()
        if Invoice.objects.filter(order=order):
            invoice = Invoice.objects.get(order=order)
        else:
            invoice = Invoice.objects.create(order=order, shop=order.buyer_shop, created_at=order.created_at)
        order_products = OrderProduct.objects.filter(order=order)
        total_qty = 0
        for item in order_products:
            total_qty = total_qty + item.qty
        order_total = num2text(order.total_price)
        order_total_qty = num2text(total_qty)

        context = {
            'total_qty': total_qty,
            'order_total_qty': order_total_qty,
            'order_total': order_total,
            'order_products': order_products,
            'order': order,
            'invoice': invoice,
        }
        return render(request, 'siteadmin/invoice_template_2.html', context)


class InvoicePDF2View(View):

    def get(self, request, *args, **kwargs):
        order = Order.objects.get(id=kwargs.get('id'))
        order.save()
        if Invoice.objects.filter(order=order):
            invoice = Invoice.objects.get(order=order)
        else:
            invoice = Invoice.objects.create(order=order, shop=order.buyer_shop, created_at=order.created_at)
        order_products = OrderProduct.objects.filter(order=order)
        total_qty = 0
        for item in order_products:
            total_qty = total_qty + item.qty
        order_total = num2text(order.total_price)
        order_total_qty = num2text(total_qty)

        responce = HttpResponse(content_type='application/pdf')
        responce['Content-Disposition'] = 'inline; filename=Накладная' + \
            str(order.buyer_shop.title)+'.pdf'
        responce['Content-Transfer-Encoding'] = 'binary'

        context = {
            'total_qty': total_qty,
            'order_total_qty': order_total_qty,
            'order_total': order_total,
            'order_products': order_products,
            'order': order,
            'invoice': invoice,
        }

        html_string = render_to_string('siteadmin/invoice_template_2.html', context)
        html = HTML(string=html_string, base_url=request.build_absolute_uri())

        result = html.write_pdf()

        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            responce.write(output.read())

        return responce


class EditInvoiceView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            order = Order.objects.get(id=kwargs.get('id'))
            if Invoice.objects.filter(order=order):
                invoice = Invoice.objects.get(order=order)
            else:
                invoice = Invoice.objects.create(order=order, shop=order.buyer_shop, created_at=order.created_at)
            form = EditInvoiceForm(request.POST or None, instance=invoice)
            context = {
                'invoice': invoice,
                'form': form,
            }
            return render(request, 'siteadmin/edit_invoice.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            order = Order.objects.get(id=kwargs.get('id'))
            if Invoice.objects.filter(order=order):
                invoice = Invoice.objects.get(order=order)
            else:
                invoice = Invoice.objects.create(order=order, shop=order.buyer_shop, created_at=order.created_at)

            if request.method == "POST":
                form = EditInvoiceForm(request.POST or None, instance=invoice)
                if form.is_valid():
                    form.save()
                    return redirect('admin_shop_invoice_pdf', order.id)
            else:
                form = EditInvoiceForm(request.POST or None, instance=invoice)

            context = {
                'invoice': invoice,
                'form': form,
            }
            return render(request, 'siteadmin/edit_invoice.html', context)

        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class AddOrderPayInvView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            order = Order.objects.get(id=kwargs.get('order_id'))
            shop = ShopBuyer.objects.get(id=kwargs.get('shop_id'))
            if not PaymentInvoice.objects.filter(shop=shop, finish_making=False):
                pay_inv = PaymentInvoice.objects.create(shop=shop, finish_making=False)
            else:
                pay_inv = PaymentInvoice.objects.get(shop=shop, finish_making=False)

            if not OrdersPaymentInvoice.objects.filter(pay_invoice=pay_inv, order=order):
                order_pay_inv = OrdersPaymentInvoice.objects.create(pay_invoice=pay_inv, order=order)
                products = OrderProduct.objects.filter(order=order_pay_inv.order)
                for item in products:
                    if OrderProductPaymentInvoice.objects.filter(product=item.product, pay_invoice=pay_inv):
                        ord_product = OrderProductPaymentInvoice.objects.get(product=item.product, pay_invoice=pay_inv)
                        ord_product.qty = ord_product.qty + item.qty
                        ord_product.save()
                    elif not OrderProductPaymentInvoice.objects.filter(product=item.product, pay_invoice=pay_inv):
                        ord_product = OrderProductPaymentInvoice.objects.create(product=item.product, pay_invoice=pay_inv)
                        ord_product.qty = ord_product.qty + item.qty
                        ord_product.save()

            pay_inv.save()
            return redirect("admin_shop_orders_detail", shop.id)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class DeleteOrderPayInvView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            order = Order.objects.get(id=kwargs.get('order_id'))
            shop = ShopBuyer.objects.get(id=kwargs.get('shop_id'))
            if not PaymentInvoice.objects.filter(shop=shop, finish_making=False):
                pay_inv = PaymentInvoice.objects.create(shop=shop, finish_making=False)
            else:
                pay_inv = PaymentInvoice.objects.get(shop=shop, finish_making=False)

            if OrdersPaymentInvoice.objects.filter(pay_invoice=pay_inv, order=order):
                order_pay_inv = OrdersPaymentInvoice.objects.create(pay_invoice=pay_inv, order=order)
                products = OrderProduct.objects.filter(order=order_pay_inv.order)
                for item in products:
                    if OrderProductPaymentInvoice.objects.filter(product=item.product, pay_invoice=pay_inv):
                        ord_product = OrderProductPaymentInvoice.objects.get(product=item.product, pay_invoice=pay_inv)
                        ord_product.qty = ord_product.qty - item.qty
                        ord_product.save()
                        if ord_product.qty == 0:
                            ord_product.delete()
                OrdersPaymentInvoice.objects.filter(pay_invoice=pay_inv, order=order).delete()

            pay_inv.save()
            return redirect("admin_shop_orders_detail", shop.id)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class EditPaymentInvoiceView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            id_p_i =  kwargs.get('id')
            shop = ShopBuyer.objects.get(id=kwargs.get('shop_id'))
            if id_p_i == 0:
                if PaymentInvoice.objects.filter(shop=shop, finish_making=False):
                    pay_inv = PaymentInvoice.objects.get(shop=shop, finish_making=False)
                else:
                    return redirect('admin_all_pay_inv')
            else:
                if PaymentInvoice.objects.filter(pk=id_p_i, shop=shop):
                    pay_inv = PaymentInvoice.objects.get(pk=id_p_i, shop=shop)
                else:
                    return redirect('admin_all_pay_inv')

            form = EditPaymentInvoiceForm(request.POST or None, instance=pay_inv)
            context = {
                'pay_inv': pay_inv,
                'form': form,
            }
            return render(request, 'siteadmin/edit_pay_invoice.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            id_p_i =  kwargs.get('id')
            shop = ShopBuyer.objects.get(id=kwargs.get('shop_id'))
            if id_p_i == 0:
                if PaymentInvoice.objects.filter(shop=shop, finish_making=False):
                    pay_inv = PaymentInvoice.objects.get(shop=shop, finish_making=False)
                else:
                    return redirect('admin_all_pay_inv')
            else:
                if PaymentInvoice.objects.filter(pk=id_p_i, shop=shop):
                    pay_inv = PaymentInvoice.objects.get(pk=id_p_i, shop=shop)
                else:
                    return redirect('admin_all_pay_inv')
            if request.method == "POST":
                form = EditPaymentInvoiceForm(request.POST or None, instance=pay_inv)
                if form.is_valid():
                    form.save()
                    return redirect('admin_shop_pay_invoice_pdf', shop.id, 0)
            else:
                form = EditInvoiceForm(request.POST or None, instance=invoice)

            context = {
                'pay_inv': pay_inv,
                'form': form,
            }
            return render(request, 'siteadmin/edit_pay_invoice.html', context)

        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class PayInvoicePDFView(View):

    def get(self, request, *args, **kwargs):
        id_p_i =  kwargs.get('id')
        shop = ShopBuyer.objects.get(id=kwargs.get('shop_id'))
        if id_p_i == 0:
            if PaymentInvoice.objects.filter(shop=shop, finish_making=False):
                pay_inv = PaymentInvoice.objects.get(shop=shop, finish_making=False)
            else:
                return redirect('admin_all_pay_inv')
        else:
            if PaymentInvoice.objects.filter(pk=id_p_i, shop=shop):
                pay_inv = PaymentInvoice.objects.get(pk=id_p_i, shop=shop)
            else:
                return redirect('admin_all_pay_inv')

        pay_inv_prod = OrderProductPaymentInvoice.objects.filter(pay_invoice=pay_inv)
        pay_inv_qty_text = num2text(pay_inv.qty)
        pay_inv_total_text = num2text(pay_inv.total_price)
        responce = HttpResponse(content_type='application/pdf')
        responce['Content-Disposition'] = 'inline; filename=Счет на оплату' + \
            str(shop.title)+'.pdf'
        responce['Content-Transfer-Encoding'] = 'binary'

        context = {
            'pay_inv_prod': pay_inv_prod,
            'pay_inv': pay_inv,
            'pay_inv_qty_text': pay_inv_qty_text,
            'pay_inv_total_text': pay_inv_total_text
        }

        html_string = render_to_string('siteadmin/pay_invoice_template.html', context)
        html = HTML(string=html_string)

        result = html.write_pdf()

        pay_inv.finish_making = True
        pay_inv.save()

        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            responce.write(output.read())

        return responce


class PayInvoicePDF2View(View):

    def get(self, request, *args, **kwargs):
        id_p_i =  kwargs.get('id')
        shop = ShopBuyer.objects.get(id=kwargs.get('shop_id'))
        if id_p_i == 0:
            if PaymentInvoice.objects.filter(shop=shop, finish_making=False):
                pay_inv = PaymentInvoice.objects.get(shop=shop, finish_making=False)
            else:
                return redirect('admin_all_pay_inv')
        else:
            if PaymentInvoice.objects.filter(pk=id_p_i, shop=shop):
                pay_inv = PaymentInvoice.objects.get(pk=id_p_i, shop=shop)
            else:
                return redirect('admin_all_pay_inv')

        pay_inv_prod = OrderProductPaymentInvoice.objects.filter(pay_invoice=pay_inv)
        pay_inv_qty_text = num2text(pay_inv.qty)
        pay_inv_total_text = num2text(pay_inv.total_price)
        responce = HttpResponse(content_type='application/pdf')
        responce['Content-Disposition'] = 'inline; filename=Счет на оплату' + \
            str(shop.title)+'.pdf'
        responce['Content-Transfer-Encoding'] = 'binary'

        context = {
            'pay_inv_prod': pay_inv_prod,
            'pay_inv': pay_inv,
            'pay_inv_qty_text': pay_inv_qty_text,
            'pay_inv_total_text': pay_inv_total_text
        }

        html_string = render_to_string('siteadmin/pay_invoice_template_2.html', context)
        html = HTML(string=html_string, base_url=request.build_absolute_uri())

        result = html.write_pdf()

        pay_inv.finish_making = True
        pay_inv.save()

        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            responce.write(output.read())

        return responce


class PayInvoiceView(View):

    def get(self, request, *args, **kwargs):
        id_p_i =  kwargs.get('id')
        shop = ShopBuyer.objects.get(id=kwargs.get('shop_id'))
        if id_p_i == 0:
            if PaymentInvoice.objects.filter(shop=shop, finish_making=False):
                pay_inv = PaymentInvoice.objects.get(shop=shop, finish_making=False)
            else:
                return redirect('admin_all_pay_inv')
        else:
            if PaymentInvoice.objects.filter(pk=id_p_i, shop=shop):
                pay_inv = PaymentInvoice.objects.get(pk=id_p_i, shop=shop)
            else:
                return redirect('admin_all_pay_inv')
        pay_inv_prod = OrderProductPaymentInvoice.objects.filter(pay_invoice=pay_inv)
        pay_inv_qty_text = num2text(pay_inv.qty)
        pay_inv_total_text = num2text(pay_inv.total_price)

        context = {
            'pay_inv_prod': pay_inv_prod,
            'pay_inv': pay_inv,
            'pay_inv_qty_text': pay_inv_qty_text,
            'pay_inv_total_text': pay_inv_total_text

        }
        return render(request, 'siteadmin/pay_invoice_template.html', context)


class PayInvoiceDetailView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            pay_inv = PaymentInvoice.objects.filter(finish_making=True).order_by('-id')
            pay_inv_prod = OrderProductPaymentInvoice.objects.filter(pay_invoice__in=pay_inv).order_by('-id')
            paginator = Paginator(pay_inv, 15)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context = {
                'pay_inv_prod': pay_inv_prod,
                'page_obj': page_obj,
            }
            return render(request, 'siteadmin/pay_inv_detail.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class DeletePayInvoiceView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            PaymentInvoice.objects.get(id=kwargs.get('id')).delete()

            return redirect("admin_all_pay_inv")
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class DeleteOrderView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            order = Order.objects.get(id=kwargs.get('order_id'))
            order_products = OrderProduct.objects.filter(order=order)
            prepared_products_per_day = PreparedProductsPerDay.objects.get(created_at=order.created_at)

            for item in order_products:
                item.save()
                pre_product = PreparedProduct.objects.get(prepared_products_p_d=prepared_products_per_day, product=item.product)
                pre_product.qty = pre_product.qty + item.qty
                pre_product.sale_qty = pre_product.sale_qty - item.qty
                pre_product.save()

            realization_orders = Order.objects.filter(finish_making=True, created_at=order.created_at, buying_type='realization').order_by('-id')
            realization_order_products = OrderProduct.objects.filter(order__in=realization_orders).order_by('-id')

            orders = Order.objects.filter(finish_making=True, created_at=order.created_at, buying_type='simple').order_by('-id')
            order_products = OrderProduct.objects.filter(order__in=orders).order_by('-id')

            orders_kaspi = Order.objects.filter(finish_making=True, created_at=order.created_at, buying_type='simple', pay='kaspi').order_by('-id')
            orders_cash = Order.objects.filter(finish_making=True, created_at=order.created_at, buying_type='simple', pay='cash').order_by('-id')

            refunds = Refund.objects.filter(finish_making=True, created_at=order.created_at).order_by('-id')
            refund_products = RefundProduct.objects.filter(refund__in=refunds).order_by('-id')
            stocks = Stocks.objects.filter(finish_making=True, created_at=order.created_at).order_by('-id')
            stock_products = StocksProduct.objects.filter(stocks__in=stocks).order_by('-id')

            for_day = ForDay.objects.get(created_at=order.created_at)

            order_sum = 0
            order_debt = 0
            order_qty = 0

            order_sum_kaspi = 0
            order_debt_kaspi = 0

            order_sum_cash = 0
            order_debt_cash = 0

            order_sum_r = 0
            order_realization_debt = 0
            order_qty_r = 0

            refund_sum = 0
            refund_qty = 0
            stocks_sum = 0
            stocks_qty = 0

            for item in orders:
                if item.paid == True:
                    order_sum = order_sum + item.total_price
                elif item.paid == False:
                    order_debt = order_debt + item.total_price
                order_qty = order_qty + 1

            for item in orders_kaspi:
                if item.paid == True:
                    order_sum_kaspi = order_sum_kaspi + item.total_price
                elif item.paid == False:
                    order_debt_kaspi = order_debt_kaspi + item.total_price

            for item in orders_cash:
                if item.paid == True:
                    order_sum_cash = order_sum_cash + item.total_price
                elif item.paid == False:
                    order_debt_cash = order_debt_cash + item.total_price

            for item in realization_orders:
                if item.paid == True:
                    order_sum_r = order_sum_r + item.total_price
                elif item.paid == False:
                    order_realization_debt = order_realization_debt + item.total_price
                order_qty_r = order_qty_r + 1

            for item in refunds:
                refund_sum = refund_sum + item.total_price
                refund_qty = refund_qty + 1

            for item in stocks:
                stocks_sum = stocks_sum + item.total_price
                stocks_qty = stocks_qty + 1

            for_day.order_cash = order_sum_cash
            for_day.order_kaspi = order_sum_kaspi

            for_day.order_debt_cash = order_debt_cash
            for_day.order_debt_kaspi = order_debt_kaspi

            for_day.order = order_sum
            for_day.order_debt = order_debt
            for_day.order_qty = order_qty
            for_day.order_realization = order_sum_r
            for_day.order_realization_debt = order_realization_debt
            for_day.order_realization_qty = order_qty_r
            for_day.refund = refund_sum
            for_day.refund_qty = refund_qty
            for_day.stocks = stocks_sum
            for_day.stocks_qty = stocks_qty
            for_day.save()


            order.delete()
            url = kwargs.get('url')
            url_id = kwargs.get('url_id')
            if url_id == 0:
                return redirect(url)
            else:
                return redirect(url, url_id)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class IngredientCategoryView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            category = IngredientCategory.objects.all()

            context = {
                'category': category
            }
            return render(request, 'siteadmin/ingredient_category_detail.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class AddIngredientCategoryView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            form = IngredientCategoryForm(request.POST or None)
            context = {
                'form': form,
            }
            return render(request, 'siteadmin/add_ingredient_category.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            if request.method == "POST":
                form = IngredientCategoryForm(request.POST or None)
                if form.is_valid():
                    form.save()
                    return redirect('ingredient_category_detail')
            else:
                form = CategoryForm(request.POST or None)

            context = {
                'form': form,
            }
            return render(request, 'siteadmin/add_category.html', context)

        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class EditIngredientCategoryView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            c_ingredient = IngredientCategory.objects.get(id=kwargs.get('id'))
            form = IngredientCategoryForm(request.POST or None, instance=c_ingredient)
            context = {
                'c_ingredient' : c_ingredient,
                'form': form,
            }
            return render(request, 'siteadmin/edit_ingredient_category.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            c_ingredient = IngredientCategory.objects.get(id=kwargs.get('id'))
            if request.method == "POST":
                form = IngredientCategoryForm(request.POST or None, instance=c_ingredient)
                if form.is_valid():
                    form.save()
                    id = kwargs.get('id')
                    return redirect('ingredient_category_edit', id)
            else:
                form = IngredientCategoryForm(request.POST or None, instance=c_ingredient)

            context = {
                'c_ingredient' : c_ingredient,
                'form': form,
            }
            return render(request, 'siteadmin/edit_ingredient_category.html', context)

        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class DeleteIngredientCategoryView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            category = IngredientCategory.objects.get(id=kwargs.get('id')).delete()

            return redirect("ingredient_category_detail")
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class IngredientView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            ingredient = Ingredient.objects.all()

            context = {
                'ingredient': ingredient
            }
            return render(request, 'siteadmin/ingredient_detail.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class EditIngredientView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            ingredient = Ingredient.objects.get(id=kwargs.get('id'))
            form = IngredientForm(request.POST or None, instance=ingredient)
            IngredientFormset = inlineformset_factory(Ingredient, UnderIngredient, extra=1, fk_name='product', fields=('ingredient', 'gross', 'unit_of_measurement'))
            formset = IngredientFormset(instance=ingredient)
            context = {
                'formset': formset,
                'ingredient': ingredient,
                'form': form,
            }
            return render(request, 'siteadmin/edit_ingredient.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            ingredient = Ingredient.objects.get(id=kwargs.get('id'))
            IngredientFormset = inlineformset_factory(Ingredient, UnderIngredient, extra=1, fk_name='product', fields=('ingredient', 'gross', 'unit_of_measurement'))
            if request.method == "POST":
                form = IngredientForm(request.POST or None, instance=ingredient)
                formset = IngredientFormset(request.POST or None, instance=ingredient)
                if formset.is_valid():
                    formset.save()
                if form.is_valid():
                    form.save()
                id = kwargs.get('id')
                return redirect('edit_ingredient_detail', id)
            else:
                form = IngredientForm(request.POST or None, instance=ingredient)
                formset = IngredientFormset(instance=ingredient)

            context = {
                'formset': formset,
                'ingredient': ingredient,
                'form': form,
            }
            return render(request, 'siteadmin/edit_ingredient.html', context)

        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class AddIngredientView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            form = IngredientForm(request.POST or None)
            context = {
                'form': form,
            }
            return render(request, 'siteadmin/add_ingredient_detail.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            if request.method == "POST":
                form = IngredientForm(request.POST or None)
                if form.is_valid():
                    form.save()
                id = form.instance.id
                return redirect('edit_ingredient_detail', id)
            else:
                formset = IngredientFormset(instance=ingredient)

            context = {
                'form': form,
            }
            return render(request, 'siteadmin/add_ingredient_detail.html', context)

        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class DeleteIngredientView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            ingredient = Ingredient.objects.get(id=kwargs.get('id')).delete()

            return redirect("ingredient_detail")
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class ProductIngredientView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            products = TechCard.objects.all()

            context = {
                'products': products
            }
            return render(request, 'siteadmin/techcart_detail.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class EditIngredientView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            tech_card = TechCard.objects.get(id=kwargs.get('id'))
            form = TechCardForm(request.POST or None, instance=tech_card)
            TechCardIngredientFormset = inlineformset_factory(TechCard, TechCardIngredient, extra=1, fields=('ingredient', 'gross', 'unit_of_measurement', 'cost_price'))
            formset = TechCardIngredientFormset(instance=tech_card)
            context = {
                'formset': formset,
                'tech_card': tech_card,
                'form': form,
            }
            return render(request, 'siteadmin/edit_tech_card.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            tech_card = TechCard.objects.get(id=kwargs.get('id'))

            TechCardIngredientFormset = inlineformset_factory(TechCard, TechCardIngredient, extra=1, fields=('ingredient', 'gross', 'unit_of_measurement', 'cost_price'))
            if request.method == "POST":
                form = TechCardForm(request.POST or None, instance=tech_card)
                formset = TechCardIngredientFormset(request.POST or None, instance=tech_card)
                if formset.is_valid():
                    formset.save()
                if form.is_valid():
                    form.save()
                id = kwargs.get('id')
                return redirect('edit_edit_tech_card_detail', id)
            else:
                form = TechCardForm(request.POST or None, instance=tech_card)
                formset = TechCardIngredientFormset(instance=tech_card)

            context = {
                'formset': formset,
                'tech_card': tech_card,
                'form': form,
            }
            return render(request, 'siteadmin/edit_tech_card.html', context)

        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class AddProductIngredientView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            form = TechCardForm(request.POST or None)
            context = {
                'form': form,
            }
            return render(request, 'siteadmin/add_product_ingredient_detail.html', context)
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            if request.method == "POST":
                form = TechCardForm(request.POST or None)
                if form.is_valid():
                    form.save()
                id = form.instance.id
                return redirect('edit_edit_tech_card_detail', id)
            else:
                formset = IngredientFormset(instance=ingredient)

            context = {
                'form': form,
            }
            return render(request, 'siteadmin/add_product_ingredient_detail.html', context)

        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")


class DeleteProductIngredientView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated == True and request.user.is_staff == True:
            tech_card = TechCard.objects.get(id=kwargs.get('id')).delete()

            return redirect("tech_card_detail")
        elif request.user.is_authenticated == True and request.user.is_staff == False:
            return redirect("/")
        else:
            return redirect("/administrator/login")
