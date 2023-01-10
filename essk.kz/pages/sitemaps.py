from django.contrib import sitemaps
from django.urls import reverse
from products.models import *


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['main','login', 'registration', 'cart', 'all_categories', 'about_company', 'certificates', 'partners', 'delivery', 'payment', 'refund', 'contacts']

    def location(self, item):
        return reverse(item)


class CategorySitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return Category.objects.all()


class ProductSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return Product.objects.all()
