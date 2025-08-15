from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('products', views.LoanProductViewSet, basename='loan-product')
router.register('applications', views.LoanApplicationViewSet, basename='loan-application')
router.register('', views.LoanViewSet, basename='loan')

urlpatterns = [
    path('', include(router.urls)),
]
