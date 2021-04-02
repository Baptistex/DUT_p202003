from django import template

from produit.forms import ContactForm

register = template.Library()


@register.simple_tag
def feedback_form():
    return ContactForm()