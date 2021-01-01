from django.utils import timezone

from rest_framework import fields, serializers

import uuid

from dfam_api_app.models import *



class DataFileSubReadSerializer(serializers.ModelSerializer):
    pass

class DataFileSubWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataFileSub
        fields = (            
            "file",
            "data_file_type",            
            "owner",
            "submitter"
        )

    def create(self, validated_data):
        data_file_sub = DataFileSub()        
        data_file_sub.data_file_type = validated_data.get("data_file_type")
        data_file_sub.owner = validated_data.get("owner")
        data_file_sub.submitter = validated_data.get("submitter")
        data_file_sub.updated = timezone.now()        
        data_file_sub.uuid = str(uuid.uuid4())
        data_file_sub.save()        
        return data_file_sub
    
    def update(self, instance, validated_data):
        pass