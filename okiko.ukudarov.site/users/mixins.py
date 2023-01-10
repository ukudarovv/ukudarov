from django.views.generic import View

from .models import *


class StudentMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            student = Student.objects.get(user=request.user)
        else:
            student = Student.objects.all()
        self.student = student
        return super().dispatch(request, *args, **kwargs)


class AdminMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if UniversityAdministrator.objects.filter(user=request.user):
                admin = True
            else:
                admin = False
        else:
            admin = False

        self.admin = admin
        return super().dispatch(request, *args, **kwargs)
