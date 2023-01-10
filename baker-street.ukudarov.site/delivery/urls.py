from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import *


urlpatterns = [
    path('', DeliveryBaseView.as_view(), name='delivery_base'),
    path('change/delivery/<int:id>/<int:status>/', ChangeStatusDelivery.as_view(), name='change_status_delivery'),
    path('login/', DeliveryLoginView.as_view(), name='delivery_login'),
    path('profile/', DeliverymanProfileView.as_view(), name='delivery_profile'),
    path('profile/edit/', EditDeliverymanProfileView.as_view(), name='delivery_profile_edit'),

    path('shop/<int:id>/', ShopContactDetailView.as_view(), name='shop_detail'),
    path('shop/edit/<int:id>/', EditShopContactView.as_view(), name='shop_edit'),
    path('shop/edit_admin/<int:id>/', EditShopAdminContactView.as_view(), name='shop_edit_admin'),

    path('shop/<int:id>/orders/', ShopOrdersDetailView.as_view(), name='shop_orders_detail'),
    path('shop/<int:id>/refunds/', ShopRefundsDetailView.as_view(), name='shop_refunds_detail'),
    path('shop/<int:id>/stocks/', ShopStocksDetailView.as_view(), name='shop_stocks_detail'),

    path('shop/<int:id>/make_order/', MakeOrderChoiceView.as_view(), name='make_order'),
    path('shop/<int:id>/complete_order/', CompleteOrderView.as_view(), name='complete_order'),
    path('shop/add/<int:shop_id>/<int:id>/<int:order_id>/', AddProductToOrder.as_view(), name='add_to_order'),
    path('shop/delete/<int:shop_id>/<int:id>/<int:order_id>/', DeleteProductToOrder.as_view(), name='delete_from_order'),
    path('shop/change/<int:shop_id>/<int:id>/', ChangeQtyOrder.as_view(), name='change_product_qty'),

    path('shop/refund/<int:id>/make_refund/', MakeRefundChoiceView.as_view(), name='make_refund'),
    path('shop/refund/<int:id>/complete_order/', CompleteRefundView.as_view(), name='complete_refund'),
    path('shop/refund/add/<int:shop_id>/<int:id>/<int:refund_id>/', AddProductToRefund.as_view(), name='add_to_refund'),
    path('shop/refund/delete/<int:shop_id>/<int:id>/<int:refund_id>/', DeleteProductToRefund.as_view(), name='delete_from_refund'),
    path('shop/refund/change/<int:shop_id>/<int:id>/', ChangeQtyRefund.as_view(), name='refund_change_product_qty'),


    path('shop/stocks/<int:id>/make_stocks/', MakeStocksChoiceView.as_view(), name='make_stocks'),
    path('shop/stocks/<int:id>/complete_stocks/', CompleteStocksView.as_view(), name='complete_stocks'),
    path('shop/stocks/add/<int:shop_id>/<int:id>/<int:stocks_id>/', AddProductToStocks.as_view(), name='add_to_stocks'),
    path('shop/stocks/delete/<int:shop_id>/<int:id>/<int:stocks_id>/', DeleteProductToStocks.as_view(), name='delete_from_stocks'),
    path('shop/stocks/change/<int:shop_id>/<int:id>/', ChangeQtyStocks.as_view(), name='stocks_change_product_qty'),

    # path('shop/new/<int:id>/', NewShopView.as_view(), name='new_shop'),
    # path('shop/new/', NewShopAdminView.as_view(), name='new_shop_admin'),
    path('shop/new/', NewShopView.as_view(), name='new_shop_admin'),
]
