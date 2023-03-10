from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import *
from mainapp import views


urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('shops/', ShopsView.as_view(), name='shops_view'),
    path('search/', SearchView.as_view(), name='search_view'),
    path('plan_1/', MainPlanView.as_view(), name='main_plan'),
    path('main_building/', MainBuildingView.as_view(), name='main_building'),
    path('block_b_1_floor/', BlockBFirstFloorView.as_view(), name='block_b_1_floor'),
    path('block_b_2_floor/', BlockBSecondFloorView.as_view(), name='block_b_2_floor'),
    path('block_c_1_floor/', BlockCFirstFloorView.as_view(), name='block_c_1_floor'),
    path('block_c_2_floor/', BlockCSecondFloorView.as_view(), name='block_c_2_floor'),
    path('about_dina/', AboutDinaView.as_view(), name='about_dina'),
    path('about_us/', AboutUsView.as_view(), name='about_us'),
    path('p/<str:slug>/', ParentCategoryView.as_view(), name='parent_category_detail'),
    path('m/<str:slug>/', MiddleCategoryView.as_view(), name='middle_category_detail'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<str:slug>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change-qty/<str:slug>/', ChangeQTYView.as_view(), name='change_qty'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('make-order/', MakeOrderView.as_view(), name='make_order'),
    path('products/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('news/<str:slug>/', NewsDetailView.as_view(), name='news_detail'),
    path('news/', NewsView.as_view(), name='news'),
    path('shop/<str:slug>/', ShopView.as_view(), name='shop_detail'),
    path('shop_category/<int:pk>/', ShopCategoryView.as_view(), name='shop_category'),
    path('shop-product/', ShopProductDetailView.as_view(), name='shop_product_detail'),
    path('shop-service/', ShopServiceDetailView.as_view(), name='shop_service_detail'),
    path('shop-staff/', ShopStaffDetailView.as_view(), name='shop_staff_detail'),
    path('add_product/', AddProductView.as_view(), name='add_product'),
    path('add_service/', AddServiceView.as_view(), name='add_service'),
    path('edit_product/<int:pk>/', EditProductView.as_view(), name='edit_product'),
    path('edit_service/<int:pk>/', EditServiceView.as_view(), name='edit_service'),
    path('add_product_feature/', AddProductFeatureView.as_view(), name='add_product_feature'),
    path('delete-from-shop/<str:slug>/', DeleteFromShopView.as_view(), name='delete_from_shop'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page="/"), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile_update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('create_shop/', CreateShopView.as_view(), name='create_shop'),
    path('profile/orders_history/', ProfileOrderHistoryView.as_view(), name='orders_history'),
    path('add_user/', AddUserView.as_view(), name='add_user'),
    path('request_to_work_request/<str:id>/', AnswerRequestToWork2View.as_view(), name='request_to_work_request'),
    path('request_to_work/', AnswerRequestToWorkView.as_view(), name='request_to_work'),
    path('shop_order/', ShopOrdersView.as_view(), name='shop_order'),
    path('shop_request/', ShopRequestsView.as_view(), name='shop_request'),
    path('complaints/', ComplaintsView.as_view(), name='complaints'),
    path('feature_update_view/<int:pk>/', FeatureUpdateView.as_view(), name='feature_update_view'),
    path('shop_update/', ShopDetailUpdateView.as_view(), name='shop_update'),
    path('support/', SupportServiceView.as_view(), name='support'),
    path('online_camera/', OnlineView.as_view(), name='online_camera'),
    path('chg_order_status/<int:id>/', ChangeOrderStatusView.as_view(), name='chg_order_status'),
    path('chg_request_status/<int:id>/', ChangeRequestStatusView.as_view(), name='chg_request_status'),
    path('req_from_shop/', RequestFromShopView.as_view(), name='req_from_shop'),
]
