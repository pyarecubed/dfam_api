from django.utils import timezone

from rest_framework import fields, serializers

from datetime import datetime as dt
import uuid

from dfam_api_app.models import *


class DataFileSubReadSerializer(serializers.ModelSerializer):
    data_file_type = serializers.SerializerMethodField()
    data_file_sub_state = serializers.SerializerMethodField()
    submitted = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()

    class Meta:
        model = DataFileSub
        fields = (
            "id",
            "data_file_type",
            "data_file_sub_state",
            "data_file_sub_state_description",
            "submitted",
            "updated"
        )
    
    def get_data_file_type(self, instance):        
        return instance.data_file_type.display_name
    
    def get_data_file_sub_state(self, instance):
        return instance.data_file_sub_state.display_name

    def get_submitted(self, instance):
        return instance.submitted.strftime("%m/%d/%Y, %H:%M")

    def get_updated(self, instance):
        return instance.updated.strftime("%m/%d/%Y, %H:%M")

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

class UserDataFileTypeSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    display_name = serializers.SerializerMethodField()
    
    class Meta:
        model = UserDataFileType
        fields = (
            "id",        
            "display_name"
        )
    
    def get_id(self, instance):
        return instance.data_file_type.id
    
    def get_display_name(self, instance):
        return instance.data_file_type.display_name