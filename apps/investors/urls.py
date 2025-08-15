from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('portfolios', views.PortfolioViewSet, basename='portfolio')
router.register('investments', views.InvestmentViewSet, basename='investment')

urlpatterns = [
    path('', include(router.urls)),
    path('invest/', views.InvestView.as_view(), name='invest'),
]
