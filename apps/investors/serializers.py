from rest_framework import serializers
from .models import Investor, InvestorPortfolio, Investment

class InvestorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.get_full_name', read_only=True)
    class Meta:
        model = Investor
        fields = '__all__'

class InvestorPortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestorPortfolio
        fields = '__all__'

class InvestmentSerializer(serializers.ModelSerializer):
    loan_id_short = serializers.SerializerMethodField()
    class Meta:
        model = Investment
        fields = '__all__'
    def get_loan_id_short(self, obj):
        return f'LN-{str(obj.loan_id)[:8]}'

class InvestSerializer(serializers.Serializer):
    loan_id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=14, decimal_places=2)
