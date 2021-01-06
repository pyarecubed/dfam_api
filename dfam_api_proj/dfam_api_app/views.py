from django.http import Http404
from django.shortcuts import render
from django.utils import timezone

from rest_framework import filters, generics, status
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from dfam_api_app.models import *
from dfam_api_app.serializers import *

"""
whichever django imports we need to read from settings to get our uploaded files base path thing
"""

"""
endpoint/URL that 
    accepts file uploads
    renames the file to a (G)UID
    upserts a file object from models into the db
"""

"""
    get all file types for user in question
"""

"""
    get all submitted files for user in question
"""

"""
    get all entities (and columns) for a given file type
"""

"""
    update the state of a file submission
"""

class DataFileSubView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk=None, **kwargs):
        pass

    def get(self, request, pk=None, **kwargs):
        pass

    def patch(self, request, **kwargs):
        pass

    def post(self, request, **kwargs):
        request.data["owner"] = request.user.id
        data_file_sub_write_ser = DataFileSubWriteSerializer(data = request.data)
        if(data_file_sub_write_ser.is_valid()):            
            try:
                persisted_data_file_sub = data_file_sub_write_ser.save()
            except:
                return Response(
                    {"message" : "Exception saving model"},
                    status = status.HTTP_400_BAD_REQUEST
                )
            try:
                persisted_data_file_sub.file = request.FILES['file']
                persisted_data_file_sub.updated = timezone.now()
                persisted_data_file_sub.data_file_sub_state = DataFileSubState.objects.get(name = "submitted")
                persisted_data_file_sub.save()
            except:
                persisted_data_file_sub.data_file_sub_state = DataFileSubState.objects.get(name = "aborted")
                #persisted_data_file_sub.data_file_sub_state_description = ""
                persisted_data_file_sub.save()
                return Response(
                    {"message" : "Exception saving file upload"},
                    status = status.HTTP_400_BAD_REQUEST
                )                        
            return Response(
                {
                    "data_file_sub" : DataFileSubReadSerializer(persisted_data_file_sub).data,
                    "message" : "File Sub saved"
                },
                status = status.HTTP_200_OK
            )
        else:
            return Response(
                data_file_sub_write_ser.errors,
                status = status.HTTP_400_BAD_REQUEST
            )

class DataFileSubMetaRelatedView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if("fetch_related" in self.request.query_params):
            
            if(self.request.query_params["fetch_related"] is None):
                return Response(
                    status = status.HTTP_204_NO_CONTENT    
                )

            related_fetches = self.request.query_params["fetch_related"].strip().split(",")

            fetches_response = {}

            if("data_file_type" in related_fetches):
                if(self.request.user.user_data_file_type.count() > 0):
                    fetches_response["data_file_type"] = UserDataFileTypeSerializer(
                        self.request.user.user_data_file_type.all().order_by("data_file_type__name"),
                        many = True
                    ).data

            if(len(fetches_response) > 0):
                return Response(
                    fetches_response,
                    status = status.HTTP_200_OK
                )
            else:
                return Response(
                status = status.HTTP_204_NO_CONTENT
            )

        else:
            return Response(
                status = status.HTTP_204_NO_CONTENT
            )

class UserDataFileSubView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):        
        return Response(
            DataFileSubReadSerializer(                
                DataFileSub.objects.filter(owner = self.request.user).order_by("submitted"),                
                many = True
            ).data,
            status = status.HTTP_200_OK
        )