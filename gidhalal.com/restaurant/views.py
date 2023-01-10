from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, get_user_model
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import DetailView, View, TemplateView
from django.shortcuts import get_list_or_404, get_object_or_404, render
from datetime import datetime, timedelta, date
from django.forms import inlineformset_factory, modelformset_factory

from django.template.loader import get_template, render_to_string

from .models import *
from halal_site.models import *


class AdminPanelView(View):

    def get(self, request, *args, **kwargs):
        user = RestaurantUser.objects.get(user=request.user)
        restaurant = Restaurant.objects.get(id=user.restaurant.id)

        context = {
            'user': user,
            'restaurant': restaurant
        }
        return render(request, 'restaurant_panel/restaurant_page.html', context)
