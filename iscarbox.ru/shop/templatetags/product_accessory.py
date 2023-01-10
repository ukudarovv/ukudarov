from django import template
from shop.models import *

register = template.Library()


@register.simple_tag()
def product_accessory():
    return ProductAccessory.objects.filter(available=True)


@register.simple_tag()
def product_accessory_1():
    return ProductAccessory.objects.filter(available=True)[0:1]
