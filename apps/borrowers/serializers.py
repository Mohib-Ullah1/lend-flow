from rest_framework import serializers
from .models import Borrower, BorrowerProfile

class BorrowerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowerProfile
        exclude = ['borrower']

class BorrowerListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Borrower
        fields = ['id', 'email', 'phone', 'kyc_status', 'risk_score', 'risk_grade', 'full_name', 'created_at']

    def get_full_name(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.full_name
        return obj.email

class BorrowerDetailSerializer(serializers.ModelSerializer):
    profile = BorrowerProfileSerializer(read_only=True)

    class Meta:
        model = Borrower
        fields = '__all__'
        read_only_fields = ['id', 'institution', 'created_at', 'updated_at']

class BorrowerCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    date_of_birth = serializers.DateField(write_only=True)
    ssn_last4 = serializers.CharField(write_only=True, required=False, default='')
    address = serializers.JSONField(write_only=True, required=False, default=dict)
    employment_status = serializers.CharField(write_only=True, required=False, default='')
    annual_income = serializers.DecimalField(write_only=True, max_digits=14, decimal_places=2, required=False, default=0)

    class Meta:
        model = Borrower
        fields = ['email', 'phone', 'first_name', 'last_name', 'date_of_birth', 'ssn_last4', 'address', 'employment_status', 'annual_income']

    def create(self, validated_data):
        profile_data = {
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
            'date_of_birth': validated_data.pop('date_of_birth'),
            'ssn_last4': validated_data.pop('ssn_last4', ''),
            'address': validated_data.pop('address', {}),
            'employment_status': validated_data.pop('employment_status', ''),
            'annual_income': validated_data.pop('annual_income', 0),
        }
        validated_data['institution'] = self.context['request'].user.institution
        borrower = Borrower.objects.create(**validated_data)
        BorrowerProfile.objects.create(borrower=borrower, **profile_data)
        return borrower
