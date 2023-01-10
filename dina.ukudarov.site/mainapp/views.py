from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, View, TemplateView
from django.contrib.auth.models import Group
from django.shortcuts import get_list_or_404, get_object_or_404

from .mixins import CartMixin

from .forms import *

from .utils import recalc_cart

from specs.models import ProductFeatures


class MyQ(Q):

    default = 'OR'


class BaseView(CartMixin, TemplateView):
    template_name = "base.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ParentCategory.objects.all()
        context['slider'] = Slider.objects.all()
        context['news'] = News.objects.all()
        shop = Shop.objects.filter(status='ACTIVE')
        context['products'] = Product.objects.filter(shop__in=shop, status='ACTIVE', service=False).order_by('-id')
        context['cart'] = self.cart
        return context


class ShopsView(CartMixin, TemplateView):
    template_name = "shops_view.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ParentCategory.objects.all()
        context['shop'] = Shop.objects.filter(status='ACTIVE')
        context['cart'] = self.cart
        return context


class ProductDetailView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = ReviewsForm(request.POST or None)
        form_2 = RequestServiceToShopForm(request.POST or None)
        categories = ParentCategory.objects.all()
        product = Product.objects.get(slug=kwargs.get('slug'))
        reviews = Reviews.objects.filter(product=product)
        reviews_count = Reviews.objects.filter(product=product).count()
        rating = Rating.objects.filter(product=product)

        context = {
            'form': form,
            'form_2': form_2,
            'product': product,
            'rating': rating,
            'reviews': reviews,
            'reviews_count': reviews_count,
            'categories': categories,
            'cart': self.cart
        }
        return render(request, 'product_detail.html', context)

    def post(self, request, *args, **kwargs):
        categories = ParentCategory.objects.all()
        form = ReviewsForm(request.POST or None)
        form_2 = RequestServiceToShopForm(request.POST or None)
        product = Product.objects.get(slug=kwargs.get('slug'))
        customer = Customer.objects.get(user=request.user)
        reviews = Reviews.objects.filter(product=product)
        reviews_count = Reviews.objects.filter(product=product).count()
        rating = Rating.objects.filter(product=product)
        if form_2.is_valid():
            new_req = form_2.save(commit=False)
            new_req.customer = customer
            new_req.shop = product.shop
            new_req.service = product
            new_req.save()
            messages.add_message(request, messages.INFO, "Ваша заявка была отправлена!")

        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.rating = form.cleaned_data['rating']
            new_review.product = product
            new_review.customer = customer
            new_review.comment = form.cleaned_data['comment']
            new_review.save()
            messages.add_message(request, messages.INFO, "Ваш комментарий был добавлен!")
            if Rating.objects.filter(product=product):
                rating_product = Rating.objects.get(product=product)
                if form.cleaned_data['rating'] == 1:
                    rating_product.one += 1
                elif form.cleaned_data['rating'] == 2:
                    rating_product.two += 1
                elif form.cleaned_data['rating'] == 3:
                    rating_product.three += 1
                elif form.cleaned_data['rating'] == 4:
                    rating_product.four += 1
                elif form.cleaned_data['rating'] == 5:
                    rating_product.five += 1
                i = 5 * rating_product.five + 4 * rating_product.four + 3 * rating_product.three + 2 * rating_product.two + 1 * rating_product.one
                b = rating_product.five + rating_product.four + rating_product.three + rating_product.two + rating_product.one
                c = i / b
                rating_product.average_rating = c
                rating_product.save()
            else:
                rating_product = Rating.objects.create(product=product, average_rating=0)
                if form.cleaned_data['rating'] == 1:
                    rating_product.one += 1
                elif form.cleaned_data['rating'] == 2:
                    rating_product.two += 1
                elif form.cleaned_data['rating'] == 3:
                    rating_product.three += 1
                elif form.cleaned_data['rating'] == 4:
                    rating_product.four += 1
                elif form.cleaned_data['rating'] == 5:
                    rating_product.five += 1
                i = 5 * rating_product.five + 4 * rating_product.four + 3 * rating_product.three + 2 * rating_product.two + 1 * rating_product.one
                b = rating_product.five + rating_product.four + rating_product.three + rating_product.two + rating_product.one
                c = i / b
                rating_product.average_rating = c
                rating_product.save()
        context = {
            'form': form,
            'form_2': form_2,
            'product': product,
            'rating': rating,
            'reviews': reviews,
            'reviews_count': reviews_count,
            'cart': self.cart,
            'categories': categories
        }
        return render(request, 'product_detail.html', context)


class ParentCategoryView(CartMixin, DetailView):
    model = ParentCategory
    queryset = ParentCategory.objects.all()
    context_object_name = 'parent_category'
    template_name = "parent_category.html"
    slug_url_kwarg = 'slug'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ParentCategory.objects.all()
        context['cart'] = self.cart
        return context


class MiddleCategoryView(CartMixin, DetailView):
    model = MiddleCategory
    queryset = MiddleCategory.objects.all()
    context_object_name = 'middle_category'
    template_name = "middle_category.html"
    slug_url_kwarg = 'slug'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ParentCategory.objects.all()
        context['cart'] = self.cart
        return context


class SearchView(CartMixin, TemplateView):

    template_name = 'search_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('search')
        context['cart'] = self.cart
        context['categories'] = ParentCategory.objects.all()
        if query:
            shop = Shop.objects.filter(status='ACTIVE')
            products = Product.objects.filter(Q(title__icontains=query, shop__in=shop, status='ACTIVE'))
            context['search_products'] = products
            return context
        return context


class ShopCategoryView(CartMixin, TemplateView):

    template_name = 'shops_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        context['categories'] = ParentCategory.objects.all()
        category = get_object_or_404(ParentCategory, pk=kwargs.get('pk'))
        context['shop'] = Shop.objects.filter(status='ACTIVE', category=category)
        return context


class CategoryDetailView(CartMixin, DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('search')
        category = self.get_object()
        context['cart'] = self.cart
        context['categories_p'] = ParentCategory.objects.all()
        context['categories'] = ParentCategory.objects.filter(slug=category.middle_category.parent_category.slug)
        if not query and not self.request.GET:
            shop = Shop.objects.filter(status='ACTIVE')
            context['category_products'] = category.product_set.filter(shop__in=shop, status='ACTIVE').order_by('-id')
            return context
        if query:
            shop = Shop.objects.filter(status='ACTIVE')
            products = category.product_set.filter(Q(title__icontains=query, shop__in=shop, status='ACTIVE')).order_by('-id')
            context['category_products'] = products
            return context
        url_kwargs = {}
        for item in self.request.GET:
            if len(self.request.GET.getlist(item)) > 1:
                url_kwargs[item] = self.request.GET.getlist(item)
            else:
                url_kwargs[item] = self.request.GET.get(item)
        q_condition_queries = Q()
        for key, value in url_kwargs.items():
            if isinstance(value, list):
                q_condition_queries.add(Q(**{'value__in': value}), Q.OR)
            else:
                q_condition_queries.add(Q(**{'value': value}), Q.OR)
        pf = ProductFeatures.objects.filter(
            q_condition_queries
        ).prefetch_related('product', 'feature').values('product_id')
        products = Product.objects.filter(id__in=[pf_['product_id'] for pf_ in pf])
        context['category_products'] = products
        return context


class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        if product.service == False:
            cart_product, created = CartProduct.objects.get_or_create(
                user=self.cart.owner, cart=self.cart, product=product
            )
            if created:
                self.cart.products.add(cart_product)
            recalc_cart(self.cart)
            messages.add_message(request, messages.INFO, "Товар успешно добавлен")
            return HttpResponseRedirect('/cart/')
        else:
            return HttpResponseRedirect('/')


class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар успешно удален")
        return HttpResponseRedirect('/cart/')


class ChangeQTYView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
        )
        qty = int(request.POST.get('qty'))
        cart_product.qty = qty
        cart_product.save()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Кол-во успешно изменено")
        return HttpResponseRedirect('/cart/')


class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = ParentCategory.objects.all()
        context = {
            'cart': self.cart,
            'categories': categories
        }
        return render(request, 'cart.html', context)


class CheckoutView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = ParentCategory.objects.all()
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'categories': categories,
            'form': form
        }
        return render(request, 'checkout.html', context)


class RequestFromShopView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = ParentCategory.objects.all()
        form = RequestFromShopForm(request.POST or None)
        context = {
            'cart': self.cart,
            'categories': categories,
            'form': form
        }
        return render(request, 'req_from_shop.html', context)

    def post(self, request, *args, **kwargs):
        form = RequestFromShopForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, "Заявка отправлена!")
            return HttpResponseRedirect('/')
        context = {
            'form': form,
            'cart': self.cart
        }
        return render(request, 'req_from_shop.html', context)


class MakeOrderView(CartMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            for item in self.cart.products.all():
                new_order.shops.add(item.product.shop)
                OrderProduct.objects.create(
                    order=new_order,
                    shop=item.product.shop,
                    product=item.product,
                    qty=item.qty,
                    final_price=item.final_price
                )
                if not OrderForShop.objects.filter(order=new_order, shop=item.product.shop):
                    OrderForShop.objects.create(
                        order=new_order,
                        shop=item.product.shop,
                        status='STATUS_NEW'
                    )
            for item in self.cart.products.all():
                order_product = OrderProduct.objects.filter(order=new_order, shop=item.product.shop)
                for item_p in order_product:
                    if not OrderForShop.objects.filter(order=new_order, shop=item_p.product.shop,
                                                       product=item_p):
                            print(item_p.product.title)
                            order_for_shop_add = OrderForShop.objects.get(order=new_order, shop=item_p.product.shop)
                            order_for_shop_add.product.add(item_p)
                            order_for_shop_add.total_products = order_product.count()
                            order_for_shop_add.final_price += item_p.final_price
                            order_for_shop_add.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            context = {
                'new_order': new_order,
                'cart': self.cart,
            }
            return render(request, 'order-complete.html', context)
        return HttpResponseRedirect('/checkout/')


class LoginView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        categories = ParentCategory.objects.all()
        context = {
            'form': form,
            'categories': categories,
            'cart': self.cart
        }
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.get(username=username)
            UserPassword.objects.filter(user=user).update(password=password)
            user = authenticate(
                username=username, password=password
            )
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        categories = ParentCategory.objects.all()
        context = {
            'form': form,
            'cart': self.cart,
            'categories': categories
        }
        return render(request, 'login.html', context)


class RegistrationView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        categories = ParentCategory.objects.all()
        context = {
            'form': form,
            'categories': categories,
            'cart': self.cart
        }
        return render(request, 'registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Customer.objects.create(
                user=new_user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email']
            )
            UserPassword.objects.create(
                user=new_user,
                password=form.cleaned_data['password']
            )
            user = authenticate(
                username=new_user.username, password=form.cleaned_data['password']
            )
            login(request, user)
            return HttpResponseRedirect('/')
        categories = Category.objects.all()
        context = {
            'form': form,
            'categories': categories,
            'cart': self.cart
        }
        return render(request, 'registration.html', context)


class ProfileOrderHistoryView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        orders = Order.objects.filter(customer=customer).order_by('-created_at')
        context = {
            'customer': customer,
            'orders': orders,
            'cart': self.cart
        }
        return render(request, 'profile_order_history.html', context)


class ShopView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        shop = Shop.objects.filter(slug=slug)
        products = Product.objects.filter(shop__in=shop, status='ACTIVE')
        context = {
            'products': products,
            'shop': shop,
            'cart': self.cart
        }
        return render(request, 'shop_detail.html', context)


class AddProductView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = AddProductForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        shop = Shop.objects.filter(customer=customer)
        context = {
            'shop': shop,
            'form': form,
            'customer': customer,
            'cart': self.cart
        }
        return render(request, 'shop_add_product.html', context)

    def post(self, request, *args, **kwargs):
        form = AddProductForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        shop = Shop.objects.get(customer=customer)

        if form.is_valid():
            if not Product.objects.filter(title=form.cleaned_data['title'], shop=shop):
                product = Product.objects.create(
                    shop=shop,
                    category=form.cleaned_data['category'],
                    title=form.cleaned_data['title'],
                    image=request.FILES['image'],
                    description=form.cleaned_data['description'],
                    price=form.cleaned_data['price']
                )
                image_2 = request.FILES.get('image_2')
                image_3 = request.FILES.get('image_3')
                image_4 = request.FILES.get('image_4')
                if image_2:
                    product.image_2=request.FILES['image_2']
                if image_3:
                    product.image_3=request.FILES['image_3']
                if image_4:
                    product.image_4=request.FILES['image_4']
                product.save()
                rating_product = Rating.objects.create(product=product, average_rating=0)
                messages.add_message(request, messages.INFO, 'Товар был добавлен!')
                return redirect("/shop-product")
            else:
                messages.add_message(request, messages.INFO, 'Товар с данным название уже существует у вас в магазине!')
                customer = Customer.objects.get(user=request.user)
                context = {
                    'form': form,
                    'customer': customer,
                    'cart': self.cart
                }
                return render(request, 'shop_add_product.html', context)
        context = {
            'form': form,
            'customer': customer,
            'cart': self.cart
        }
        return render(request, 'shop_add_product.html', context)


class AddServiceView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = AddServiceForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        shop = Shop.objects.filter(customer=customer)
        context = {
            'shop': shop,
            'form': form,
            'customer': customer,
            'cart': self.cart
        }
        return render(request, 'shop_add_service.html', context)

    def post(self, request, *args, **kwargs):
        form = AddServiceForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        shop = Shop.objects.get(customer=customer)

        if form.is_valid():
            if not Product.objects.filter(title=form.cleaned_data['title'], shop=shop):
                product = Product.objects.create(
                    shop=shop,
                    category=form.cleaned_data['category'],
                    title=form.cleaned_data['title'],
                    image=request.FILES['image'],
                    description=form.cleaned_data['description'],
                    price=form.cleaned_data['price'],
                    contractual_price=form.cleaned_data['contractual_price'],
                    service=True
                )
                image_2 = request.FILES.get('image_2')
                image_3 = request.FILES.get('image_3')
                image_4 = request.FILES.get('image_4')
                if image_2:
                    product.image_2=request.FILES['image_2']
                if image_3:
                    product.image_3=request.FILES['image_3']
                if image_4:
                    product.image_4=request.FILES['image_4']
                product.save()
                rating_product = Rating.objects.create(product=product, average_rating=0)
                messages.add_message(request, messages.INFO, 'Услуга была добавлена!')
                return redirect("/shop-service")
            else:
                messages.add_message(request, messages.INFO, 'Услуга с данным название уже существует у вас в магазине!')
                customer = Customer.objects.get(user=request.user)
                context = {
                    'form': form,
                    'customer': customer,
                    'cart': self.cart
                }
                return render(request, 'shop_add_service.html', context)
        context = {
            'form': form,
            'customer': customer,
            'cart': self.cart
        }
        return render(request, 'shop_add_service.html', context)


class EditProductView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs.get('pk'))
        form = EditProductForm(request.POST or None, instance=product)
        customer = Customer.objects.get(user=request.user)
        categories = Category.objects.all()
        context = {
            'product': product,
            'customer': customer,
            'categories': categories,
            'form': form,
            'cart': self.cart
        }
        return render(request, 'product_edit.html', context)

    def post(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        categories = Category.objects.all()
        shop = Shop.objects.filter(customer=customer)
        if request.method == "POST":
            product = get_object_or_404(Product, pk=kwargs.get('pk'))
            form = EditProductForm(request.POST or None, instance=product)
            if form.is_valid():
                product = form.save(commit=False)
                image = request.FILES.get('image')
                image_2 = request.FILES.get('image_2')
                image_3 = request.FILES.get('image_3')
                image_4 = request.FILES.get('image_4')
                if image:
                    product.image=request.FILES['image']
                if image_2:
                    product.image_2=request.FILES['image_2']
                if image_3:
                    product.image_3=request.FILES['image_3']
                if image_4:
                    product.image_4=request.FILES['image_4']
                product.save()
                return redirect('/shop-product', pk=product.pk)
        else:
            product = get_object_or_404(Product, pk=kwargs.get('pk'))
            form = EditProductForm(request.POST or None, instance=product)

        context = {
            'product': product,
            'categories': categories,
            'shop': shop,
            'form': form,
            'customer': customer,
        }
        return render(request, 'product_edit.html', context)


class EditServiceView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs.get('pk'))
        form = EditServiceForm(request.POST or None, instance=product)
        customer = Customer.objects.get(user=request.user)
        categories = Category.objects.all()
        context = {
            'product': product,
            'customer': customer,
            'categories': categories,
            'form': form,
            'cart': self.cart
        }
        return render(request, 'service_edit.html', context)

    def post(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        categories = Category.objects.all()
        shop = Shop.objects.filter(customer=customer)
        if request.method == "POST":
            product = get_object_or_404(Product, pk=kwargs.get('pk'))
            form = EditServiceForm(request.POST or None, instance=product)
            if form.is_valid():
                product = form.save(commit=False)
                image = request.FILES.get('image')
                image_2 = request.FILES.get('image_2')
                image_3 = request.FILES.get('image_3')
                image_4 = request.FILES.get('image_4')
                if image:
                    product.image=request.FILES['image']
                if image_2:
                    product.image_2=request.FILES['image_2']
                if image_3:
                    product.image_3=request.FILES['image_3']
                if image_4:
                    product.image_4=request.FILES['image_4']
                product.save()
                return redirect('/shop-service', pk=product.pk)
        else:
            product = get_object_or_404(Product, pk=kwargs.get('pk'))
            form = EditServiceForm(request.POST or None, instance=product)

        context = {
            'product': product,
            'categories': categories,
            'shop': shop,
            'form': form,
            'customer': customer,
        }
        return render(request, 'service_edit.html', context)


class FeatureUpdateView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs.get('pk'))
        categories = Category.objects.all()
        context = {
            'product': product,
            'categories': categories,
            'cart': self.cart
        }
        return render(request, 'feature_view.html', context)


class AddProductFeatureView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        shop = Shop.objects.get(customer=customer)
        product = Product.objects.filter(shop=shop).order_by("-id")[0:1]
        categories = Category.objects.all()
        context = {
            'categories': categories,
            'product': product,
            'customer': customer,
            'cart': self.cart
        }
        return render(request, 'add_product_feature.html', context)


class ProfileView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        categories = ParentCategory.objects.all()
        shop = Shop.objects.filter(customer=customer)
        request_to_work = RequestToWork.objects.filter(customer=customer, active=False)

        context = {
            'request_to_work': request_to_work,
            'shop': shop,
            'customer': customer,
            'categories': categories,
            'cart': self.cart
        }
        users_in_group = Group.objects.get(name="Продавец").user_set.all()
        if request.user in users_in_group:
            return render(request, 'seller_profile.html', context)
        else:
            return render(request, 'profile.html', context)


class ShopProductDetailView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        shop = Shop.objects.filter(customer=customer)
        products = Product.objects.filter(shop__in=shop, service=False)
        context = {
            'customer': customer,
            'products': products,
            'cart': self.cart
        }
        return render(request, 'shop_product_detail.html', context)



class ShopServiceDetailView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        shop = Shop.objects.filter(customer=customer)
        products = Product.objects.filter(shop__in=shop, service=True).order_by('-id')
        context = {
            'customer': customer,
            'products': products,
            'cart': self.cart
        }
        return render(request, 'shop_service_detail.html', context)


class ShopStaffDetailView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        shop = Shop.objects.filter(customer=customer)
        context = {
            'customer': customer,
            'shop': shop,
            'cart': self.cart
        }
        return render(request, 'shop_staff_detail.html', context)


class ProfileUpdateView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        form = UpdateProfileForm(request.POST or None, instance=customer)
        context = {
            'form': form,
            'customer': customer,
            'cart': self.cart
        }
        return render(request, 'profile_update.html', context)

    def post(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        form = UpdateProfileForm(request.POST or None, instance=customer)

        if form.is_valid():
            customer = Customer.objects.get(user=request.user)
            user = User.objects.get(username=request.user.username)
            if form.cleaned_data['first_name'] != "":
                customer.first_name = form.cleaned_data['first_name']
                user.first_name = form.cleaned_data['first_name']
            if form.cleaned_data['last_name'] != "":
                customer.last_name = form.cleaned_data['last_name']
                user.last_name = form.cleaned_data['last_name']
            if form.cleaned_data['address'] != "":
                customer.address = form.cleaned_data['address']
            if form.cleaned_data['email'] != "":
                customer.email = form.cleaned_data['email']
                user.email = form.cleaned_data['email']
            if form.cleaned_data['sex'] != "":
                customer.sex = form.cleaned_data['sex']
            if form.cleaned_data['phone'] != "":
                customer.phone = form.cleaned_data['phone']
            user.save()
            customer.save()
            messages.add_message(request, messages.INFO, 'Данные были обновлены!')
            return redirect("/profile")
        context = {
            'form': form,
            'cart': self.cart
        }
        return render(request, 'profile_update.html', context)


class CreateShopView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = CreateShopForm(request.POST or None, request.FILES)
        customer = Customer.objects.get(user=request.user)

        context = {
            'form': form,
            'customer': customer,
            'cart': self.cart
        }
        return render(request, 'create_shop.html', context)

    def post(self, request, *args, **kwargs):
        form = CreateShopForm(request.POST or None, request.FILES)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_shop = form.save(commit=False)
            new_shop.save()
            for item in form.cleaned_data['category']:
                new_shop.category.add(item)
            new_shop.customer.add(Customer.objects.get(user=request.user))
            g = Group.objects.get(
                name='Продавец')
            g.user_set.add(request.user)
            Customer.objects.filter(user=request.user).update(job='DIRECTOR')

            messages.add_message(request, messages.INFO, 'Магазин был создан!')
            return redirect("/profile")
        context = {
            'form': form,
            'customer': customer,
            'cart': self.cart
        }
        return render(request, 'create_shop.html', context)


class AddUserView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = SearchUserForm(request.POST or None, request.FILES)
        customer = Customer.objects.get(user=request.user)

        context = {
            'form': form,
            'customer': customer,
            'cart': self.cart
        }
        return render(request, 'user_search.html', context)

    def post(self, request, *args, **kwargs):
        form = SearchUserForm(request.POST or None, request.FILES)
        if form.is_valid():
            user = Customer.objects.get(user=request.user)
            request_1 = RequestToWork.objects.filter(customer=user).exists()
            if request_1:
                messages.add_message(request, messages.INFO, 'Ранее вы уже отправляли запрос данному пользователю!')
            else:
                try:
                    username = form.cleaned_data['q']
                    user = User.objects.get(username=username)

                    customer = Customer.objects.get(user=user.id)
                    customer_request = Customer.objects.get(user=request.user)
                    shop = Shop.objects.get(customer=customer_request)

                    RequestToWork.objects.create(
                        customer=customer,
                        shop=shop,
                        job=form.cleaned_data['job']
                    )
                    messages.add_message(request, messages.INFO, 'Запрос на добавление был отправлен!')
                    return redirect("/profile")
                except User.DoesNotExist:
                    messages.add_message(request, messages.INFO, 'Данный пользователь не был найден!')

        context = {
            'form': form,
            'cart': self.cart
        }
        return render(request, 'user_search.html', context)


class AnswerRequestToWorkView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = AnswerRequestToWorkForm(request.POST or None, request.FILES)
        customer = Customer.objects.get(user=request.user)
        request_to_work = RequestToWork.objects.filter(customer=customer, active=False)
        context = {
            'request_to_work': request_to_work,
            'form': form,
            'customer': customer,
            'cart': self.cart
        }
        return render(request, 'answer_to_work.html', context)


class AnswerRequestToWork2View(CartMixin, View):

    def post(self, request, *args, **kwargs):
        form = AnswerRequestToWorkForm(request.POST or None, request.FILES)

        if form.is_val():
            customer = Customer.objects.get(user=request.user)
            RequestToWork.objects.filter(customer=customer).update(yes_or_no=form.cleaned_data['yes_or_no'])
            request_to_work = RequestToWork.objects.get(customer=customer)

            if form.cleaned_data['yes_or_no'] == 'YES':
                shop_id = kwargs.get('id')
                customer = Customer.objects.get(user=request.user)
                shop = Shop.objects.get(id=shop_id)
                shop.customer.add(customer)
                shop.save()
                RequestToWork.objects.filter(shop=shop, customer=customer).update(active=True)

            elif form.cleaned_data['yes_or_no'] == 'NO':
                shop_id = kwargs.get('id')
                shop = Shop.objects.get(id=shop_id)
                r = RequestToWork.objects.filter(shop=shop, customer=customer)
                r.delete()
            g = Group.objects.get(
                name='Продавец')
            g.user_set.add(request.user)
            if request_to_work.job == "Продавец":
                Customer.objects.filter(user=request.user).update(job='SELLER')
            elif request_to_work.job == "Ремонтник":
                Customer.objects.filter(user=request.user).update(job='REPAIRER')
            elif request_to_work.job == "Бухгалтер":
                Customer.objects.filter(user=request.user).update(job='ACCOUNTANT')

            messages.add_message(request, messages.INFO, 'Ответ был отправлен!')
            return redirect("/profile")
        context = {
            'form': form,
            'cart': self.cart
        }
        return render(request, 'answer_to_work.html', context)


class ShopOrdersView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        shop = Shop.objects.filter(customer=customer)
        orders = OrderForShop.objects.filter(shop__in=shop).order_by('-order')
        context = {
            'orders': orders,
            'shop': shop,
            'customer': customer,
            'cart': self.cart
        }
        return render(request, 'order_shop.html', context)


class ShopRequestsView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        shop = Shop.objects.filter(customer=customer)
        requests = RequestServiceToShop.objects.filter(shop__in=shop).order_by('-created_at')
        context = {
            'requests': requests,
            'shop': shop,
            'customer': customer,
            'cart': self.cart
        }
        return render(request, 'requests_shop.html', context)


class ChangeRequestStatusView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        request_id = kwargs.get('id')
        request = RequestServiceToShop.objects.get(id=request_id)
        status_request = request.POST.get('status_request')
        if status_request == "STATUS_COMPLETED":
            for item in request.service.all():
                item.product.order_qty += 1
                item.product.save()



        request.status = status_request
        request.save()
        messages.add_message(request, messages.INFO, "Данные успешно изменены!")
        return HttpResponseRedirect('/shop_request/')


class ChangeOrderStatusView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        order_id = kwargs.get('id')
        order = OrderForShop.objects.get(id=order_id)
        status_order = request.POST.get('status_order')
        if status_order == "STATUS_COMPLETED":
            for item in order.product.all():
                item.product.order_qty += 1
                item.product.save()



        order.status = status_order
        order.save()
        messages.add_message(request, messages.INFO, "Данные успешно изменены!")
        return HttpResponseRedirect('/shop_order/')


class ComplaintsView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = ComplaintsForm(request.POST or None, request.FILES)
        customer = Customer.objects.get(user=request.user)
        context = {
            'form': form,
            'customer': customer,
            'cart': self.cart
        }
        return render(request, 'сomplaints.html', context)

    def post(self, request, *args, **kwargs):
        form = ComplaintsForm(request.POST or None, request.FILES)
        if form.is_valid():
            customer = Customer.objects.get(user=request.user)
            new_complaints = form.save(commit=False)
            new_complaints.user = customer
            new_complaints.save()
            messages.add_message(request, messages.INFO, 'Жалоба была отправлен!')
            return redirect("/profile")
        context = {
            'form': form,
            'cart': self.cart
        }
        return render(request, 'сomplaints.html', context)


class ShopDetailUpdateView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        shop = get_object_or_404(Shop, customer=customer)
        form = ShopDetailUpdateForm(request.POST or None, instance=shop)
        context = {
            'shop': shop,
            'form': form,
            'customer': customer,
            'cart': self.cart
        }
        return render(request, 'shop_detail_update.html', context)

    def post(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        shop = get_object_or_404(Shop, customer=customer)
        form = ShopDetailUpdateForm(request.POST or None, instance=shop)

        if form.is_valid():
            customer = Customer.objects.get(user=request.user)
            shop = Shop.objects.get(customer=customer)
            if form.cleaned_data['category'] != "":
                for item in form.cleaned_data['category']:
                    shop.category.add(item)
            shop_image = request.FILES.get('shop_image')
            if shop_image:
                shop.shop_image = request.FILES['shop_image']
            if form.cleaned_data['description'] != "":
                shop.description = form.cleaned_data['description']
            if form.cleaned_data['shop_email'] != "":
                shop.shop_email = form.cleaned_data['shop_email']
            if form.cleaned_data['shop_phone'] != "":
                shop.shop_phone = form.cleaned_data['shop_phone']
            if form.cleaned_data['instagram'] != "":
                shop.instagram = form.cleaned_data['instagram']
            if form.cleaned_data['vk'] != "":
                shop.vk = form.cleaned_data['vk']
            if form.cleaned_data['facebook'] != "":
                shop.facebook = form.cleaned_data['facebook']
            if form.cleaned_data['whatsapp'] != "":
                shop.whatsapp = form.cleaned_data['whatsapp']
            if form.cleaned_data['telegram'] != "":
                shop.telegram = form.cleaned_data['telegram']
            shop.save()
            messages.add_message(request, messages.INFO, 'Данные магазина были обновлены!')
            return redirect("/profile")
        context = {
            'customer': customer,
            'form': form,
            'cart': self.cart
        }
        return render(request, 'shop_detail_update.html', context)


class SupportServiceView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = SupportServiceForm(request.POST or None, request.FILES)
        customer = Customer.objects.get(user=request.user)
        context = {
            'form': form,
            'customer': customer,
            'cart': self.cart
        }
        return render(request, 'support.html', context)

    def post(self, request, *args, **kwargs):
        form = SupportServiceForm(request.POST or None, request.FILES)
        if form.is_valid():
            customer = Customer.objects.get(user=request.user)
            new_support = form.save(commit=False)
            new_support.user = customer
            if form.cleaned_data['email'] == "":
                new_support.email = customer.email
            new_support.save()
            messages.add_message(request, messages.INFO, 'Заявка была отправлена!')
            return redirect("/profile")
        context = {
            'form': form,
            'cart': self.cart
        }
        return render(request, 'support.html', context)


class MainPlanView(CartMixin, TemplateView):
    template_name = "main_plan.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class MainBuildingView(CartMixin, TemplateView):
    template_name = "main_building.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class BlockBFirstFloorView(CartMixin, TemplateView):
    template_name = "block_b_1_floor.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class BlockBSecondFloorView(CartMixin, TemplateView):
    template_name = "block_b_2_floor.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class BlockCFirstFloorView(CartMixin, TemplateView):
    template_name = "block_c_1_floor.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class BlockCSecondFloorView(CartMixin, TemplateView):
    template_name = "block_c_2_floor.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class AboutDinaView(CartMixin, TemplateView):
    template_name = "about_dina.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content'] = AboutDina.objects.all()
        context['cart'] = self.cart
        return context


class AboutUsView(CartMixin, TemplateView):
    template_name = "about_us.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content'] = AboutUs.objects.all()
        context['cart'] = self.cart
        return context


class DeleteFromShopView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        product.delete()
        messages.add_message(request, messages.INFO, "Товар успешно удален")
        return HttpResponseRedirect('/shop-product/')


class NewsDetailView(CartMixin, DetailView):

    model = News
    context_object_name = 'news'
    template_name = 'news_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ParentCategory.objects.all()
        context['cart'] = self.cart
        return context


class NewsView(CartMixin, TemplateView):
    template_name = "news.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ParentCategory.objects.all()
        context['news'] = News.objects.all()
        context['cart'] = self.cart
        return context


class OnlineView(CartMixin, TemplateView):
    template_name = "online_camera.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context
