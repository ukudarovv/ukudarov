from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import *


urlpatterns = [
    path('', AdminBaseView.as_view(), name='admin_base'),
    path('users/', UsersDetailView.as_view(), name='admin_users'),
    path('shop_admins/', ShopAdminsDetailView.as_view(), name='admin_shop_admins'),

    path('shops/', ShopsView.as_view(), name='admin_shops'),
    path('shops/delete/<int:id>', DeleteShopView.as_view(), name='admin_shops_delete'),
    path('shops/<int:id>/', ShopContactDetailView.as_view(), name='admin_shop_detail'),
    path('shops/edit/<int:id>/', EditShopContactView.as_view(), name='admin_shop_edit'),
    path('shops/edit_admin/<int:id>/', EditShopAdminContactView.as_view(), name='admin_shop_edit_admin'),

    path('shops/<int:id>/orders/', ShopOrdersDetailView.as_view(), name='admin_shop_orders_detail'),
    path('shops/<int:id>/refunds/', ShopRefundsDetailView.as_view(), name='admin_shop_refunds_detail'),
    path('shops/<int:id>/stocks/', ShopStocksDetailView.as_view(), name='admin_shop_stocks_detail'),

    path('shops/new/', NewShopView.as_view(), name='admin_new_shop_admin'),

    path('deliveryman/', DeliverymanView.as_view(), name='admin_deliveryman'),
    path('deliveryman/delete/<int:id>', DeleteDeliverymanView.as_view(), name='admin_deliveryman_delete'),
    path('deliveryman/edit/<int:id>/', EditDeliverymanView.as_view(), name='admin_deliveryman_edit'),
    path('deliveryman/add/', AddDeliverymanView.as_view(), name='admin_deliveryman_add'),
    path('products/', ProductsView.as_view(), name='admin_products'),
    path('products/add/', AddProductView.as_view(), name='admin_add_products'),
    path('products/edit/<int:id>/', EditProductView.as_view(), name='admin_edit_products'),
    path('products/delete/<int:id>/', DeleteProductView.as_view(), name='admin_delete_products'),
    path('categories/', CategoryView.as_view(), name='admin_categories'),
    path('categories/add/', AddCategoryView.as_view(), name='admin_add_categories'),
    path('categories/delete/<int:id>', DeleteCategoryView.as_view(), name='admin_categories_delete'),
    path('change/pay/<int:id>/<int:status>/<str:url>/', ChangeStatusPay.as_view(), name='change_status_pay_admin'),
    path('next_day/prepared_products', PreProductsView.as_view(), name='next_prepared_products'),
    path('next_day/add/prepared_product', NextAddPreparedProductView.as_view(), name='next_add_prepared_product'),
    path('login/', AdminLoginView.as_view(), name='admin_login'),
    path('orders/', OrdersDetailView.as_view(), name='admin_orders'),
    path('realization_orders/', RealizationOrdersDetailView.as_view(), name='admin_realization_orders'),
    path('refunds/', RefundsDetailView.as_view(), name='admin_refunds'),
    path('stocks/', StocksDetailView.as_view(), name='admin_stocks'),
    path('add/prepared_product', AddPreparedProductView.as_view(), name='add_prepared_product'),
    path('edit/prepared_product', EditPreparedProductView.as_view(), name='edit_prepared_product'),


    path('shops/<int:id>/invoice', InvoiceView.as_view(), name='admin_shop_invoice'),
    path('shops/<int:id>/invoice_2', Invoice2View.as_view(), name='admin_shop_invoice_2'),
    path('shops/<int:id>/invoice/pdf/', InvoicePDFView.as_view(), name='admin_shop_invoice_pdf'),
    path('shops/<int:id>/invoice/pdf_2/', InvoicePDF2View.as_view(), name='admin_shop_invoice_pdf_2'),

    path('shops/invoice/edit/pdf/<int:id>/', EditInvoiceView.as_view(), name='admin_shop_invoice_edit_pdf'),


    path('shops/pay_invoice/add/<int:shop_id>/<int:order_id>/', AddOrderPayInvView.as_view(), name='admin_add_order_pay_inv'),
    path('shops/pay_invoice/delete/<int:shop_id>/<int:order_id>/', DeleteOrderPayInvView.as_view(), name='admin_delete_order_pay_inv'),
    path('shops/pay_invoice/new/<int:shop_id>/<int:id>/', EditPaymentInvoiceView.as_view(), name='admin_shop_pay_inv_edit'),
    path('shops/pay_invoice/pdf/<int:shop_id>/<int:id>/', PayInvoicePDFView.as_view(), name='admin_shop_pay_invoice_pdf'),
    path('shops/pay_invoice/pdf_2/<int:shop_id>/<int:id>/', PayInvoicePDF2View.as_view(), name='admin_shop_pay_invoice_pdf_2'),
    path('shops/pay_invoice/<int:shop_id>/<int:id>/', PayInvoiceView.as_view(), name='admin_shop_pay_inv'),
    path('shops/pay_invoice/all/', PayInvoiceDetailView.as_view(), name='admin_all_pay_inv'),
    path('shops/pay_invoice/delete/<int:id>/', DeletePayInvoiceView.as_view(), name='admin_delete_pay_inv'),

    path('order/delete/<int:order_id>/<str:url>/<int:url_id>/', DeleteOrderView.as_view(), name='delete_order'),

    path('shops/ingredient_categories/all/', IngredientCategoryView.as_view(), name='ingredient_category_detail'),
    path('shops/ingredient_categories/add/', AddIngredientCategoryView.as_view(), name='ingredient_category_add'),
    path('shops/ingredient_categories/edit/<int:id>/', EditIngredientCategoryView.as_view(), name='ingredient_category_edit'),
    path('shops/ingredient_categories/delete/<int:id>/', DeleteIngredientCategoryView.as_view(), name='ingredient_category_delete'),

    path('shops/ingredient/all/', IngredientView.as_view(), name='ingredient_detail'),
    path('shops/ingredient/add/', AddIngredientView.as_view(), name='ingredient_add'),
    path('shops/ingredient/delete/<int:id>/', DeleteIngredientView.as_view(), name='ingredient_delete'),
    path('shops/ingredient/edit/<int:id>/', EditIngredientView.as_view(), name='edit_ingredient_detail'),


    path('shops/tech_card/all/', ProductIngredientView.as_view(), name='tech_card_detail'),
    path('shops/tech_card/add/', AddProductIngredientView.as_view(), name='tech_card_add'),
    path('shops/tech_card/delete/<int:id>/', DeleteIngredientView.as_view(), name='tech_card_delete'),
    path('shops/tech_card/edit/<int:id>/', EditIngredientView.as_view(), name='edit_edit_tech_card_detail'),
]
