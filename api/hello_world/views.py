from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.

class HelloWorld(TemplateView):
    template_name = "HelloWorld.html"