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
from restaurant.models import *



class MainView(View):

    def get(self, request, *args, **kwargs):

        restaurants = Restaurant.objects.filter(is_active=True)
        categories = CategoryRestaurant.objects.filter(is_active=True)

        context = {
            'restaurants': restaurants,
            'categories': categories
        }
        return render(request, 'index.html', context)


class AllCategoryDetailView(View):

    def get(self, request, *args, **kwargs):
        restaurants = Restaurant.objects.filter(is_active=True)
        categories = CategoryRestaurant.objects.filter(is_active=True)

        context = {
            'restaurants': restaurants,
            'categories': categories
        }
        return render(request, 'category_page.html', context)


class CategoryDetailView(View):

    def get(self, request, *args, **kwargs):
        category = CategoryRestaurant.objects.get(id=kwargs.get('id'), is_active=True)
        restaurants = Restaurant.objects.filter(category=category, is_active=True)
        categories = CategoryRestaurant.objects.filter(is_active=True)

        context = {
            'restaurants': restaurants,
            'category': category,
            'categories': categories
        }
        return render(request, 'category_page.html', context)


class RestaurantDetailView(View):

    def get(self, request, *args, **kwargs):
        restaurant = Restaurant.objects.get(id=kwargs.get('id'), is_active=True)
        if Links.objects.filter(restaurant=restaurant):
            links = Links.objects.get(restaurant=restaurant)
        else:
            links = None

        worktimes = OpenningTime.objects.filter(restaurant=restaurant)
        products = RestaurantProduct.objects.filter(restaurant=restaurant, is_active=True)
        categories = []
        categories_id = []
        for item in products:
            if not item.category.title in categories:
                categories.append(item.category.title)
                categories_id.append(item.category.id)

        context = {
            'restaurant': restaurant,
            'links': links,
            'worktimes': worktimes,
            'products': products,
            'categories': categories,
            'categories_id': categories_id
        }
        return render(request, 'restraunt_page.html', context)
