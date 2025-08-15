from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.core.permissions import IsTenantUser
from .models import Investor, InvestorPortfolio, Investment
from .serializers import InvestorPortfolioSerializer, InvestmentSerializer, InvestSerializer

class PortfolioViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InvestorPortfolioSerializer
    permission_classes = [IsTenantUser]

    def get_queryset(self):
        return InvestorPortfolio.objects.filter(institution=self.request.user.institution)

class InvestmentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InvestmentSerializer
    permission_classes = [IsTenantUser]

    def get_queryset(self):
        return Investment.objects.filter(institution=self.request.user.institution)

class InvestView(APIView):
    permission_classes = [IsTenantUser]

    def post(self, request):
        serializer = InvestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        from apps.loans.models import Loan
        try:
            loan = Loan.objects.get(id=serializer.validated_data['loan_id'], institution=request.user.institution, status='active')
        except Loan.DoesNotExist:
            return Response({'error': 'Active loan not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Get or create investor + portfolio
        investor, _ = Investor.objects.get_or_create(user=request.user, defaults={'institution': request.user.institution})
        portfolio, _ = InvestorPortfolio.objects.get_or_create(investor=investor, defaults={'institution': request.user.institution})

        amount = serializer.validated_data['amount']
        share = (amount / loan.principal_amount * 100)

        investment = Investment.objects.create(
            institution=request.user.institution,
            portfolio=portfolio,
            loan=loan,
            amount_invested=amount,
            share_percentage=min(share, 100),
        )

        portfolio.total_invested += amount
        portfolio.current_value += amount
        portfolio.save()

        return Response(InvestmentSerializer(investment).data, status=status.HTTP_201_CREATED)
