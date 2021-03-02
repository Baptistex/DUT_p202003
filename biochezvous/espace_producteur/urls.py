from django.urls import path
from . import views

urlpatterns = [    
    path('producteur/', views.producteurs, name='producteur'),

]