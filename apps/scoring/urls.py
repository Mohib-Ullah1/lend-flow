from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('scores', views.CreditScoreViewSet, basename='credit-score')

urlpatterns = [
    path('', include(router.urls)),
    path('run/', views.ScoreApplicationView.as_view(), name='score-application'),
]
