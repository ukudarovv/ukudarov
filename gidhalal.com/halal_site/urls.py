from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import *
from restaurant.views import *


urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('restaurant/<int:id>/', RestaurantDetailView.as_view(), name='restaurant_detail'),
    path('category/all/', AllCategoryDetailView.as_view(), name='all_category_detail'),
    path('category/<int:id>/', CategoryDetailView.as_view(), name='category_detail'),
    path('admin_panel/', AdminPanelView.as_view(), name='admin_panel'),
]
