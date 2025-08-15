from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.ReportViewSet, basename='report')

urlpatterns = [
    path('generate/', views.GenerateReportView.as_view(), name='generate-report'),
    path('', include(router.urls)),
]
