from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('checks', views.KYCVerificationViewSet, basename='kyc-check')

urlpatterns = [
    path('', include(router.urls)),
    path('run/', views.RunKYCView.as_view(), name='run-kyc'),
]
