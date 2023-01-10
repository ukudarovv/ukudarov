from django import template
from landing.models import Contacts, ContactForm

register = template.Library()


@register.simple_tag()
def get_contacts():
    return Contacts.objects.all()
