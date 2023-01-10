from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


from .models import *
from .forms import *
from shop.models import Product


def index(request):
    carousels = Carousel.objects.all()
    contacts = Contacts.objects.all()
    products = Product.objects.filter(available=True)
    seo = SEO.objects.all()

    form = ContactsFrom(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        data = {
            'first_name': form.cleaned_data['first_name'],
            'phone_number': form.cleaned_data['phone_number'],
            'message': form.cleaned_data['message']
        }

        subject, from_email, to = 'Форма заявки [iscarbox.ru]', 'support@iscarbox.ru', '9kudarov9@gmail.com'
        html_content = render_to_string("landing/email.html", data)
        msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        form = form.save()
        return redirect('index')

    context = {
        'carousels': carousels,
        'contacts': contacts,
        'form': form,
        'products': products,
        'seo': seo,
    }

    return render(request, 'landing/base.html', context)


def develiry(request):
    develiry = Develiry.objects.all()
    seo = SEO.objects.all()
    return render(request, 'landing/delivery.html', {'develiry': develiry, 'seo': seo})


def paymentmethods(request):
    paymentmethods = Paymentmethods.objects.all()
    seo = SEO.objects.all()
    return render(request, 'landing/payment_methods.html', {'paymentmethods': paymentmethods, 'seo': seo})


def purchasereturns(request):
    purchasereturns = Purchasereturns.objects.all()
    seo = SEO.objects.all()
    return render(request, 'landing/purchase_returns.html', {'purchasereturns': purchasereturns, 'seo': seo})


def sitepolicy(request):
    sitepolicy = Sitepolicy.objects.all()
    seo = SEO.objects.all()
    return render(request, 'landing/site_policy.html', {'sitepolicy': sitepolicy, 'seo': seo})
