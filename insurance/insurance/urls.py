from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('insurance-pricing/', views.insurance_pricing_view, name='insurance_pricing'),
    path('success/', views.success_view, name='success'),
]
