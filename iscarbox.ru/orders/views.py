from django.shortcuts import render
from .models import *
from shop.models import *
from landing.models import *
from django.http import JsonResponse
from .forms import ProductQuantityUpdate, ProductIsActiveUpdate, OrderCreateForm


def basket_adding(request):
    seo = SEO.objects.all()
    session_key = request.session.session_key

    if request.method == 'POST':
        form_a = ProductAddBasket(request.POST, prefix='add')
        id = form_q.cleaned_data['id']
        quantity = form_a.cleaned_data['quantity']
        product = form_a.cleaned_data['product']
        product_material = form_a.cleaned_data['product_material']
        product_thread = form_a.cleaned_data['product_thread']
        product_border = form_a.cleaned_data['product_border']
        product_accessory = form_a.cleaned_data['product_accessory']

        if form_a.is_valid():
            new_product = ProductInBasket.objects.get_or_create(session_key=session_key, product=product, product_material=material, product_thread=thread, product_border=border, product_accessory=accessory, defaults={"quantity":quantity})

            if not created:
                new_product.quantity += int(quantity)
                new_product.save(force_update=True)


def cart(request):
    seo = SEO.objects.all()
    session_key = request.session.session_key

    if request.method == 'POST':
        form_q = ProductQuantityUpdate(request.POST, prefix='update')
        if form_q.is_valid():
            id = form_q.cleaned_data['id']
            product = form_q.cleaned_data['product']
            quantity = form_q.cleaned_data['quantity']
            ProductInBasket.objects.filter(session_key=session_key, id=id, product=product).update(quantity=quantity)
            products_in_basket = ProductInBasket.objects.filter(session_key=session_key, id=id, product=product, is_active=True)
            total_price = 0
            for item in products_in_basket:
                total_price = item.quantity * item.price
            ProductInBasket.objects.filter(session_key=session_key, id=id, product=product).update(total_price=total_price)
    else:
        form_q = ProductQuantityUpdate(prefix='update')

    if request.method == 'POST':
        form_a = ProductIsActiveUpdate(request.POST, prefix='remove')
        form_q = ProductQuantityUpdate(prefix='update')

        if form_a.is_valid():
            id = form_a.cleaned_data['id']
            product = form_a.cleaned_data['product']
            product_material = form_a.cleaned_data['product_material']
            product_thread = form_a.cleaned_data['product_thread']
            product_border = form_a.cleaned_data['product_border']
            product_accessory = form_a.cleaned_data['product_accessory']
            ProductInBasket.objects.filter(session_key=session_key, id=id, product=product, product_material=product_material, product_thread=product_thread, product_border=product_border, product_accessory=product_accessory).delete()
    else:
        form_a = ProductIsActiveUpdate(prefix='remove')

    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)
    get_total_price = 0
    for item in products_in_basket:
        get_total_price += item.total_price

    return render(request, 'cart/detail.html', locals())


def order_create(request):
    seo = SEO.objects.all()
    session_key = request.session.session_key

    products_in_basket_count = ProductInBasket.objects.filter(session_key=session_key).count()
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)
    get_total_price = 0
    for item in products_in_basket:
        get_total_price += item.total_price

    if products_in_basket_count > 0:
        if request.method == 'POST':
            form = OrderCreateForm(request.POST)

            if form.is_valid():
                order = form.save()
                status = Status.objects.get(name='Новый')
                Order.objects.filter(id=order.id).update(status=status)
                products_in_basket = ProductInBasket.objects.filter(session_key=session_key)
                products_in_basket_count = products_in_basket.count()
                get_total_price = 0
                for item in products_in_basket:
                    get_total_price += item.total_price
                if products_in_basket_count > 0:
                    for item in products_in_basket:
                        ProductInOrder.objects.create(
                            order=order,
                            product=item.product,
                            product_material=item.product_material,
                            product_thread=item.product_thread,
                            product_border=item.product_border,
                            product_accessory=item.product_accessory,
                            price=item.price,
                            quantity=item.quantity,
                            total_price=item.total_price
                        )

                else:
                    return render(request, 'orders/order/create.html', locals())
                Order.objects.filter(id=order.id).update(total_price=get_total_price)
                ProductInBasket.objects.filter(session_key=session_key).delete()
                return render(request, 'orders/order/created.html', locals())
        else:
            form = OrderCreateForm()
    else:
        return render(request, 'orders/order/create.html', locals())
    return render(request, 'orders/order/create.html', locals())
