from django.views.generic import View
from carts.models import *


class CartMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.session.session_key:
            request.session.save()
        session_key = request.session.session_key
        if request.user.is_authenticated:
            if Cart.objects.filter(user=request.user):
                cart = Cart.objects.get(user=request.user)
            else:
                cart = Cart.objects.create(user=request.user, token=session_key)
        else:
            if Cart.objects.filter(token=session_key):
                cart = Cart.objects.get(token=session_key, for_anonymous_user=True)
            else:
                cart = Cart.objects.create(token=session_key, for_anonymous_user=True)

        self.cart = cart
        self.cart_products = CartProduct.objects.filter(cart=cart)
        self.nds = round(cart.total_price-(cart.total_price/1.12), 2)

        return super().dispatch(request, *args, **kwargs)
