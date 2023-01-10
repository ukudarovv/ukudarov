from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import *


urlpatterns = [
    path('', AllTestsView.as_view(), name='all_tests'),
    path('<int:id>/', TestsView.as_view(), name='tests_unt_subjects'),
    path('run_test/<int:id>/<int:position>/', StartTestView.as_view(), name='run_test'),
    path('end_test/<int:id>/', EndTestView.as_view(), name='end_test')
]
