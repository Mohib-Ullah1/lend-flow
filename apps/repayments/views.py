import uuid
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from apps.core.permissions import IsTenantUser
from .models import RepaymentSchedule, Payment
from .serializers import RepaymentScheduleSerializer, PaymentSerializer, MakePaymentSerializer

class RepaymentScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RepaymentScheduleSerializer
    permission_classes = [IsTenantUser]

    def get_queryset(self):
        qs = RepaymentSchedule.objects.filter(loan__institution=self.request.user.institution)
        loan_id = self.request.query_params.get('loan_id')
        if loan_id:
            qs = qs.filter(loan_id=loan_id)
        return qs

class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsTenantUser]

    def get_queryset(self):
        return Payment.objects.filter(loan__institution=self.request.user.institution)

class MakePaymentView(APIView):
    permission_classes = [IsTenantUser]

    def post(self, request):
        serializer = MakePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        from apps.loans.models import Loan
        try:
            loan = Loan.objects.get(id=serializer.validated_data['loan_id'], institution=request.user.institution)
        except Loan.DoesNotExist:
            return Response({'error': 'Loan not found.'}, status=status.HTTP_404_NOT_FOUND)

        amount = serializer.validated_data['amount']
        payment = Payment.objects.create(
            loan=loan,
            amount=amount,
            payment_method=serializer.validated_data['payment_method'],
            payment_reference=f'PAY-{uuid.uuid4().hex[:8].upper()}',
            status='completed',
            processed_at=timezone.now(),
        )

        # Apply to next pending installment
        next_inst = loan.schedule.filter(status__in=['scheduled', 'pending', 'overdue']).order_by('installment_number').first()
        if next_inst:
            next_inst.amount_paid = amount
            next_inst.status = 'paid'
            next_inst.paid_at = timezone.now()
            next_inst.save()
            payment.installment = next_inst
            payment.save(update_fields=['installment'])

        # Update loan balance
        loan.outstanding_principal -= amount
        loan.last_payment_date = timezone.now().date()
        if loan.outstanding_principal <= 0:
            loan.outstanding_principal = 0
            loan.status = 'paid_off'
        loan.save()

        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
