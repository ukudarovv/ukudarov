from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import *


urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('download/', UmarView.as_view(), name='download'),
    path('search/', SearchView.as_view(), name='search'),
    path('profile/orders/', ProfileOrdersView.as_view(), name='profile_orders'),
    path('profile/edit/', EditProfileView.as_view(), name='profile_edit'),
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(next_page="/"), name='logout'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/update/<int:id>/', CartQtyUpdate.as_view(), name='cart_update'),
    path('cart/add/<int:id>/', AddToCart.as_view(), name='add_to_cart'),
    path('cart/remove/<int:id>/', RemoveFromCart.as_view(), name='remove_from_cart'),
    path('checkout/user/', CheckoutUserView.as_view(), name='checkout_user'),
    path('checkout/company/', CheckoutCompanyView.as_view(), name='checkout_company'),
    path('checkout/thanks/', CheckoutThanksView.as_view(), name='checkout_thanks'),
    path('product/<int:id>/', ProductView.as_view(), name='product_detail'),
    path('category/all/', AllCategoriesView.as_view(), name='all_categories'),
    path('category/<int:id>/', CategoryView.as_view(), name='category_detail'),
    path('about_company/', AboutCompanyView.as_view(), name='about_company'),
    path('certificates/', CertificatesView.as_view(), name='certificates'),
    path('partners/', PartnersView.as_view(), name='partners'),
    path('delivery/', DeliveryView.as_view(), name='delivery'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('refund/', RefundView.as_view(), name='refund'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('warranty/', WarrantyView.as_view(), name='warranty'),
    path('ax_pro/', AxProView.as_view(), name='ax_pro'),
    path('publication/category/<int:id>/', PublicationByCategoryView.as_view(), name='publication_category'),
    path('publication/<int:id>/', PublicationView.as_view(), name='publication_detail'),
]
