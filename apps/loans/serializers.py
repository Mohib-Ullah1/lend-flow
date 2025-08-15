from rest_framework import serializers
from .models import LoanProduct, LoanApplication, Loan

class LoanProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanProduct
        fields = '__all__'
        read_only_fields = ['id', 'institution', 'created_at', 'updated_at']

class LoanApplicationListSerializer(serializers.ModelSerializer):
    borrower_name = serializers.SerializerMethodField()
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = LoanApplication
        fields = ['id', 'borrower_name', 'product_name', 'amount_requested', 'term_months', 'status', 'risk_grade', 'submitted_at', 'created_at']

    def get_borrower_name(self, obj):
        if hasattr(obj.borrower, 'profile'):
            return obj.borrower.profile.full_name
        return obj.borrower.email

class LoanApplicationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication
        fields = '__all__'
        read_only_fields = ['id', 'institution', 'status', 'risk_grade', 'risk_score', 'risk_factors', 'approved_at', 'rejected_at', 'disbursed_at', 'reviewed_by', 'created_at', 'updated_at']

class LoanApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication
        fields = ['borrower', 'product', 'amount_requested', 'term_months', 'purpose']

    def validate(self, data):
        product = data['product']
        if not product.min_amount <= data['amount_requested'] <= product.max_amount:
            raise serializers.ValidationError({'amount_requested': f'Must be between {product.min_amount} and {product.max_amount}'})
        if not product.min_term_months <= data['term_months'] <= product.max_term_months:
            raise serializers.ValidationError({'term_months': f'Must be between {product.min_term_months} and {product.max_term_months}'})
        return data

    def create(self, validated_data):
        validated_data['institution'] = self.context['request'].user.institution
        validated_data['interest_rate'] = validated_data['product'].base_interest_rate
        validated_data['status'] = 'submitted'
        from django.utils import timezone
        validated_data['submitted_at'] = timezone.now()
        return super().create(validated_data)

class LoanListSerializer(serializers.ModelSerializer):
    borrower_name = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = ['id', 'borrower_name', 'principal_amount', 'outstanding_principal', 'interest_rate', 'status', 'days_past_due', 'disbursement_date']

    def get_borrower_name(self, obj):
        if hasattr(obj.borrower, 'profile'):
            return obj.borrower.profile.full_name
        return obj.borrower.email

class LoanDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = ['id', 'institution', 'created_at', 'updated_at']
