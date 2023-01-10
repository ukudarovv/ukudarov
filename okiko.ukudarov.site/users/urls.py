from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import *


urlpatterns = [
    path('admin_profile/', AdminProfileView.as_view(), name='admin_profile'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page="/"), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('edit_document/', EditDocumentView.as_view(), name='edit_document'),
    path('add_document/', AddDocumentView.as_view(), name='add_document'),
    path('delete_document/<int:id>/', DeleteDocumentView.as_view(), name='delete_document'),
    path('edit_admin_profile/', EditAdminProfileView.as_view(), name='edit_admin_profile'),
    path('edit_univ_detail/', EditUnivDetailView.as_view(), name='edit_univ_detail'),
    path('edit_univ_contact/', EditUnivContactView.as_view(), name='edit_univ_contact'),
]
