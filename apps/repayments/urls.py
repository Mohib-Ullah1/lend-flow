from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('schedule', views.RepaymentScheduleViewSet, basename='schedule')
router.register('payments', views.PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
    path('make-payment/', views.MakePaymentView.as_view(), name='make-payment'),
]
