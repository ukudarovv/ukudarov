from urllib import request
from urllib.request import Request, urlopen
import openpyxl
import csv
import re
from bs4 import BeautifulSoup
import pandas as pd
from django import forms
from django.core.exceptions import ValidationError
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
from decimal import Decimal
from products.models import *
from carts.models import *
from news.models import *
from .mixins import *
from .forms import *
from addition.models import *


class MainView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all().order_by("id")
        new_products = Product.objects.all().order_by("-id")[0:16]

        category_sale = CategoryProduct.objects.filter(title='Распродажа')
        sale_products = Product.objects.filter(category_p__in=category_sale).order_by("-id")[0:16]

        category_week = CategoryProduct.objects.filter(title='Товар недели')
        week_products = Product.objects.filter(category_p__in=category_week).order_by("-id")[0:16]

        category_offers = CategoryProduct.objects.filter(title='Спецпредложение')
        offers_products = Product.objects.filter(category_p__in=category_offers).order_by("-id")[0:16]

        product_photos = ProductPhoto.objects.all()

        banners = Banner.objects.filter(is_active=True)
        publication = Publication.objects.filter(is_active=True)



        context = {
            'cart': self.cart,
            'cart_products': self.cart_products,
            'categories': categories,
            'new_products': new_products,
            'sale_products': sale_products,
            'week_products': week_products,
            'offers_products': offers_products,
            'product_photos': product_photos,
            'banners': banners,
            'publication': publication
        }
        return render(request, 'index.html', context)


class SearchView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all().order_by("id")
        query = self.request.GET.get('search')

        if query:
            products = Product.objects.filter(Q(title__icontains=query, is_active=True))
            paginator = Paginator(products, 60)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

        context = {
            'categories': categories,
            'cart': self.cart,
            'cart_products': self.cart_products,
            'page_obj': page_obj
        }
        return render(request, 'search.html', context)


class CartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all().order_by("id")

        context = {
            'categories': categories,
            'cart': self.cart,
            'cart_products': self.cart_products,
            'nds': self.nds,
        }
        return render(request, 'cart.html', context)


class AddToCart(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('id')
        product = Product.objects.get(id=product_id)

        if not CartProduct.objects.filter(cart=self.cart, product=product):
            CartProduct.objects.create(cart=self.cart, product=product, qty=1)
        self.cart.save()
        return redirect("cart")


class RemoveFromCart(CartMixin, View):

    def get(self, request, *args, **kwargs):
        cart_product_id = kwargs.get('id')
        if CartProduct.objects.filter(id=cart_product_id):
            CartProduct.objects.filter(id=cart_product_id).delete()
        else:
            return redirect("main")

        self.cart.save()
        return redirect("cart")


class ProductView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all().order_by("id")
        product_id = kwargs.get('id')
        if Product.objects.filter(id=product_id):
            product = Product.objects.get(id=product_id)
        else:
            return redirect("main")
        product_photos = ProductPhoto.objects.filter(product=product)
        feed_backs = ProductFeedback.objects.filter(product=product)
        feed_backs_count = ProductFeedback.objects.filter(product=product).count()
        form = ProductFeedbackForm(request.POST or None)
        context = {
            'categories': categories,
            'cart': self.cart,
            'cart_products': self.cart_products,
            'product': product,
            'product_photos': product_photos,
            'form': form,
            'feed_backs': feed_backs,
            'feed_backs_count': feed_backs_count,
        }
        return render(request, 'product.html', context)

    def post(self, request, *args, **kwargs):
        categories = Category.objects.all().order_by("id")
        product_id = kwargs.get('id')
        if Product.objects.filter(id=product_id):
            product = Product.objects.get(id=product_id)
        else:
            return redirect("main")

        product_photos = ProductPhoto.objects.filter(product=product)
        feed_backs = ProductFeedback.objects.filter(product=product)
        feed_backs_count = ProductFeedback.objects.filter(product=product).count()
        form = ProductFeedbackForm(request.POST or None)

        if form.is_valid():
            feed_back = ProductFeedback.objects.create()
            if request.user.is_authenticated:
                feed_back.user = request.user
            else:
                feed_back.for_anonymous_user = True
            feed_back.product = product
            feed_back.first_name = form.cleaned_data['first_name']
            feed_back.email = form.cleaned_data['email']
            feed_back.text = form.cleaned_data['text']
            feed_back.point = form.cleaned_data['point']
            feed_back.save()
            return redirect('product_detail', product_id)

        context = {
            'categories': categories,
            'cart': self.cart,
            'cart_products': self.cart_products,
            'product': product,
            'product_photos': product_photos,
            'form': form,
            'feed_backs': feed_backs,
            'feed_backs_count': feed_backs_count,
        }
        return render(request, 'product.html', context)


class CartQtyUpdate(CartMixin, View):

    def post(self, request, *args, **kwargs):
        cart_product_id = kwargs.get('id')
        qty = int(request.POST.get('qty'))
        if CartProduct.objects.filter(id=cart_product_id, cart=self.cart):
            cart_product = CartProduct.objects.get(id=cart_product_id, cart=self.cart)
        else:
            return redirect("main")
        cart_product.qty = qty
        cart_product.save()
        self.cart.save()
        return redirect("cart")


class CheckoutUserView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            if UserAddress.objects.filter(user=request.user):
                address = UserAddress.objects.get(user=request.user)
            else:
                address = UserAddress.objects.create(user=request.user)
        else:
            user = None
            address = None
        if self.cart.total_products == 0:
            return redirect("main")
        categories = Category.objects.all().order_by("id")
        area = Area.objects.all()
        form = OrderUserForm(request.POST or None)

        context = {
            'categories': categories,
            'cart': self.cart,
            'cart_products': self.cart_products,
            'nds': self.nds,
            'form': form,
            'area': area,
            'user': user,
            'address': address
        }
        return render(request, 'checkout_user.html', context)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            if UserAddress.objects.filter(user=request.user):
                address = UserAddress.objects.get(user=request.user)
            else:
                address = UserAddress.objects.create(user=request.user)
        else:
            user = None
            address = None
        if self.cart.total_products == 0:
            return redirect("main")
        categories = Category.objects.all().order_by("id")
        area = Area.objects.all()
        form = OrderUserForm(request.POST or None)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            else:
                order.for_anonymous_user = True
            order.token = request.session.session_key
            order.type = 'pe'
            order.person = form.cleaned_data['person']
            order.phone = form.cleaned_data['phone']
            order.city = form.cleaned_data['city']
            order.area = order.city.area
            order.country = order.area.country
            order.address = form.cleaned_data['address']
            order.comment = form.cleaned_data['comment']
            order.save()
            c_products = CartProduct.objects.filter(cart=self.cart)
            for item in c_products:
                product = OrderProduct.objects.create(order=order, product=item.product, qty=item.qty)
                product.save()
                item.delete()
            self.cart.delete()
            order.save()
            if request.user.is_authenticated:
                address.city = form.cleaned_data['city']
                address.area = address.city.area
                address.country = address.area.country
                address.street = form.cleaned_data['address']
                address.save()
            return redirect("checkout_thanks")

        context = {
            'categories': categories,
            'cart': self.cart,
            'cart_products': self.cart_products,
            'nds': self.nds,
            'form': form,
            'area': area,
            'user': user,
            'address': address
        }
        return render(request, 'checkout_user.html', context)


class CheckoutCompanyView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        if self.cart.total_products == 0:
            return redirect("main")
        categories = Category.objects.all().order_by("id")
        area = Area.objects.all()
        form = OrderUserForm(request.POST or None)
        form_2 = OrderCompanyForm(request.POST or None)
        form_3 = OrderBankCompanyForm(request.POST or None)

        context = {
            'categories': categories,
            'cart': self.cart,
            'cart_products': self.cart_products,
            'nds': self.nds,
            'form': form,
            'form_2': form_2,
            'form_3': form_3,
            'area': area
        }
        return render(request, 'checkout_company.html', context)

    def post(self, request, *args, **kwargs):
        if self.cart.total_products == 0:
            return redirect("main")
        categories = Category.objects.all().order_by("id")
        area = Area.objects.all()
        form = OrderUserForm(request.POST or None)
        form_2 = OrderCompanyForm(request.POST or None)
        form_3 = OrderBankCompanyForm(request.POST or None)

        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            else:
                order.for_anonymous_user = True
            order.token = request.session.session_key
            order.type = 'le'
            order.person = form.cleaned_data['person']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.city = form.cleaned_data['city']
            order.area = order.city.area
            order.country = order.area.country
            order.address = form.cleaned_data['address']
            order.comment = form.cleaned_data['comment']
            order.save()
            c_products = CartProduct.objects.filter(cart=self.cart)
            for item in c_products:
                product = OrderProduct.objects.create(order=order, product=item.product, qty=item.qty)
                product.save()
                item.delete()
            self.cart.delete()
            order.save()
            company = form_2.save(commit=False)
            company.title = form_2.cleaned_data['title']
            company.address = form_2.cleaned_data['address']
            company.iin_bin = form_2.cleaned_data['iin_bin']
            company.phone = form.cleaned_data['phone']
            company.email = form.cleaned_data['email']
            company.save()
            c_address = CompanyAddress.objects.create(
                company=company,
                country=order.area.country,
                area=order.city.area,
                city=order.city,
                address=form_2.cleaned_data['address']
            )
            user_company = CompanyContact.objects.create()
            if request.user.is_authenticated:
                user_company.user = request.user
            else:
                user_company.for_anonymous_user = True
            user_company.company = company
            user_company.person = form.cleaned_data['person']
            user_company.phone = form.cleaned_data['phone']
            user_company.email = form.cleaned_data['email']
            user_company.save()
            order.company = company
            order.save()
            company_bank = form_3.save(commit=False)
            company_bank.company = company
            company_bank.bank_title = form_3.cleaned_data['bank_title']
            company_bank.bik = form_3.cleaned_data['bik']
            company_bank.iik = form_3.cleaned_data['iik']
            company_bank.save()
            return redirect("checkout_thanks")

        context = {
            'categories': categories,
            'cart': self.cart,
            'cart_products': self.cart_products,
            'nds': self.nds,
            'form': form,
            'form_2': form_2,
            'form_3': form_3,
            'area': area
        }
        return render(request, 'checkout_company.html', context)


class CheckoutThanksView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all().order_by("id")

        context = {
            'categories': categories,
            'cart': self.cart,
            'cart_products': self.cart_products,
        }
        return render(request, 'thanks.html', context)


class LoginView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main")
        form = LoginForm(request.POST or None)
        categories = Category.objects.all().order_by("id")

        context = {
            'form': form,
            'categories': categories,
            'cart': self.cart,
            'cart_products': self.cart_products,
        }
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main")
        form = LoginForm(request.POST or None)
        categories = Category.objects.all().order_by("id")
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_e = User.objects.get(email=email)
            user = authenticate(
                username=user_e.username, password=password
            )
            if user:
                login(request, user)
                return redirect("main")
        context = {
            'form': form,
            'categories': categories,
            'cart': self.cart,
            'cart_products': self.cart_products,
        }
        return render(request, 'login.html', context)


class RegistrationView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main")
        form = RegistrationForm(request.POST or None)
        categories = Category.objects.all().order_by("id")

        context = {
            'form': form,
            'categories': categories,
            'cart_products': self.cart_products,
            'cart': self.cart
        }
        return render(request, 'registration.html', context)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main")
        form = RegistrationForm(request.POST or None)
        categories = Category.objects.all().order_by("id")

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()

            user = authenticate(
                username=new_user.username, password=form.cleaned_data['password']
            )
            login(request, user)
            return redirect("main")
        context = {
            'form': form,
            'categories': categories,
            'cart_products': self.cart_products,
            'cart': self.cart
        }
        return render(request, 'registration.html', context)


class EditProfileView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        categories = Category.objects.all().order_by("id")
        form = UserForm(request.POST or None, instance=request.user)
        if UserAddress.objects.filter(user=request.user):
            address = UserAddress.objects.get(user=request.user)
        else:
            address = UserAddress.objects.create(user=request.user)
        form_2 = UserAddressForm(request.POST or None, instance=address)
        area = Area.objects.all()


        context = {
            'categories': categories,
            'cart': self.cart,
            'cart_products': self.cart_products,
            'form': form,
            'form_2': form_2,
            'area': area,
            'address': address
        }
        return render(request, 'edit_profile.html', context)

    def post(self, request, *args, **kwargs):
        area = Area.objects.all()
        if not request.user.is_authenticated:
            return redirect("login")
        categories = Category.objects.all().order_by("id")
        form = UserForm(request.POST or None, instance=request.user)
        if UserAddress.objects.filter(user=request.user):
            address = UserAddress.objects.get(user=request.user)
        else:
            address = UserAddress.objects.create(user=request.user)
        form_2 = UserAddressForm(request.POST or None, instance=address)

        if form.is_valid():
            user = User.objects.get(username=request.user.username)
            if form.cleaned_data['first_name'] != "":
                user.first_name = form.cleaned_data['first_name']
            if form.cleaned_data['last_name'] != "":
                user.last_name = form.cleaned_data['last_name']
            if user.email != form.cleaned_data['email']:
                if User.objects.filter(email=form.cleaned_data['email']).exists():
                    messages.add_message(request, messages.INFO, 'Данный почтовый адрес уже зарегистрирован в системе!')
                elif form.cleaned_data['email'] != "":
                    user.email = form.cleaned_data['email']
            if form.cleaned_data['phone'] != "":
                user.phone = form.cleaned_data['phone']
            user.save()
        if form_2.is_valid():
            address = UserAddress.objects.get(user=request.user)
            address.city = form_2.cleaned_data['city']
            address.area = address.city.area
            address.country = address.area.country
            address.street = form_2.cleaned_data['street']
            address.index = form_2.cleaned_data['index']
            messages.add_message(request, messages.INFO, 'Данные были обновлены12345!')
            address.save()

        messages.add_message(request, messages.INFO, 'Данные были обновлены!')
        return redirect("profile_edit")
        context = {
            'form': form,
            'form_2': form_2,
            'cart': self.cart,
            'area': area,
            'address': address
        }
        return render(request, 'edit_profile.html', context)


class ProfileOrdersView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all().order_by("id")
        if not request.user.is_authenticated:
            return redirect("login")
        orders = Order.objects.filter(user=request.user)
        order_products = OrderProduct.objects.filter(order__id__in=orders)
        context = {
            'categories': categories,
            'cart': self.cart,
            'cart_products': self.cart_products,
            'orders': orders,
            'order_products': order_products
        }
        return render(request, 'profile_orders.html', context)


class AllCategoriesView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all().order_by("id")

        context = {
            'cart': self.cart,
            'cart_products': self.cart_products,
            'categories': categories,
        }
        return render(request, 'all_categories.html', context)


class CategoryView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all().order_by("id")
        category_id = kwargs.get('id')
        category = Category.objects.get(id=category_id)
        category_p = Category.objects.filter(id=category_id).order_by("id")
        product = Product.objects.filter(category_all__in=category_p).order_by("-id")
        if Category.objects.filter(parent=category):
            categories_s = Category.objects.filter(parent=category).order_by("id")
        else:
            categories_s = Category.objects.filter(parent=category.parent).order_by("id")
        paginator = Paginator(product, 60)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'cart': self.cart,
            'cart_products': self.cart_products,
            'categories': categories,
            'categories_s': categories_s,
            'page_obj': page_obj,
            'category': category
        }
        return render(request, 'category_view.html', context)


class AboutCompanyView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all().order_by("id")

        context = {
            'cart': self.cart,
            'cart_products': self.cart_products,
            'categories': categories
        }
        return render(request, 'pages/about_company.html', context)


class CertificatesView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all().order_by("id")
        content = Certificates.objects.all()

        context = {
            'cart': self.cart,
            'cart_products': self.cart_products,
            'categories': categories,
            'content': content
        }
        return render(request, 'pages/certificates.html', context)


class PartnersView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all().order_by("id")
        content = Partners.objects.all()

        context = {
            'cart': self.cart,
            'cart_products': self.cart_products,
            'categories': categories,
            'content': content
        }
        return render(request, 'pages/partners.html', context)


class DeliveryView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all().order_by("id")

        context = {
            'cart': self.cart,
            'cart_products': self.cart_products,
            'categories': categories
        }
        return render(request, 'pages/delivery.html', context)


class PaymentView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all().order_by("id")

        context = {
            'cart': self.cart,
            'cart_products': self.cart_products,
            'categories': categories
        }
        return render(request, 'pages/payment.html', context)


class RefundView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all().order_by("id")
        content = Refund.objects.all()

        context = {
            'cart': self.cart,
            'cart_products': self.cart_products,
            'categories': categories,
            'content': content
        }
        return render(request, 'pages/refund.html', context)


class ContactsView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all().order_by("id")

        context = {
            'cart': self.cart,
            'cart_products': self.cart_products,
            'categories': categories
        }
        return render(request, 'pages/contacts.html', context)


class WarrantyView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all().order_by("id")

        context = {
            'cart': self.cart,
            'cart_products': self.cart_products,
            'categories': categories
        }
        return render(request, 'pages/warranty.html', context)


class AxProView(CartMixin, View):
    def get(self, request, *args, **kwargs):

        context = {

        }
        return render(request, 'ax_pro.html', context)


class PublicationView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all().order_by("id")
        publication_id = kwargs.get('id')

        all_category = CategoryPublication.objects.filter(is_active=True)
        last_publication = Publication.objects.filter(is_active=True).order_by("id")[:3]
        if Publication.objects.filter(id=publication_id, is_active=True):
            publication = Publication.objects.get(id=publication_id, is_active=True)
        else:
            return redirect("main")

        context = {
            'cart': self.cart,
            'cart_products': self.cart_products,
            'categories': categories,
            'all_category': all_category,
            'last_publication': last_publication,
            'publication': publication
        }
        return render(request, 'publication_view.html', context)


class PublicationByCategoryView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all().order_by("id")
        publication_category_id = kwargs.get('id')
        all_category = CategoryPublication.objects.filter(is_active=True)
        last_publication = Publication.objects.filter(is_active=True).order_by("id")[:3]
        category = CategoryPublication.objects.get(id=publication_category_id, is_active=True)
        publication = Publication.objects.filter(category=category, is_active=True)
        paginator = Paginator(publication, 60)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'cart': self.cart,
            'cart_products': self.cart_products,
            'categories': categories,
            'category': category,
            'page_obj': page_obj,
            'all_category': all_category,
            'last_publication': last_publication
        }
        return render(request, 'category_publication_view.html', context)


class UmarView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all().order_by("id")
        context = {
            'cart': self.cart,
            'cart_products': self.cart_products,
            'categories': categories,
        }
        return render(request, 'umar.html', context)
