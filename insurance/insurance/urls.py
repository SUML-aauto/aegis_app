from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Homepage
    path('support/', views.support_form, name='support_form'),  # Support form page
    path('support-success/', views.support_form_success, name='support_form_success'),  # Success page for support form
    path('insurance-pricing/', views.insurance_pricing_view, name='insurance_pricing'),  # Insurance pricing page
]
