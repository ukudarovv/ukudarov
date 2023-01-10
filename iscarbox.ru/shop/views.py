from django.shortcuts import render, get_object_or_404
from .models import *
from landing.models import *


def product_detail(request, id, slug):
    seo = SEO.objects.all()
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    product_material = ProductMaterialColor.objects.filter(product=id, available=True)
    product_material_2 = ProductMaterialColor.objects.filter(product=id, available=True)[0:1]
    product_material_3 = ProductMaterialColor.objects.filter(product=id, available=False)[0:1]
    product_thread = ProductThreadColor.objects.filter(product=id, available=True)
    product_thread_2 = ProductThreadColor.objects.filter(product=id, available=True)[0:1]
    product_thread_3 = ProductThreadColor.objects.filter(product=id, available=False)[0:1]
    product_border = ProductBorderColor.objects.filter(product=id, available=True)
    product_border_2 = ProductBorderColor.objects.filter(product=id, available=True)[0:1]
    product_border_3 = ProductBorderColor.objects.filter(product=id, available=False)[0:1]

    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    context = {
        'product': product,
        'product_material': product_material,
        'product_thread': product_thread,
        'product_border': product_border,
        'product_material_2': product_material_2,
        'product_thread_2': product_thread_2,
        'product_border_2': product_border_2,
        'product_material_3': product_material_3,
        'product_thread_3': product_thread_3,
        'product_border_3': product_border_3,
        'seo': seo,
    }
    return render(request, 'shop/product/detail.html', context)
