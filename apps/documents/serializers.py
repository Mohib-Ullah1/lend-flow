from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = ['id', 'institution', 'file_hash', 'file_size', 'created_at', 'updated_at']

class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['borrower', 'document_type', 'file']

    def create(self, validated_data):
        validated_data['institution'] = self.context['request'].user.institution
        f = validated_data['file']
        validated_data['original_filename'] = f.name
        validated_data['file_size'] = f.size
        import hashlib
        h = hashlib.sha256()
        for chunk in f.chunks():
            h.update(chunk)
        validated_data['file_hash'] = h.hexdigest()
        return super().create(validated_data)
