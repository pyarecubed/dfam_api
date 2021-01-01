from django.http import Http404
from django.shortcuts import render
from django.utils import timezone

from rest_framework import filters, generics, status
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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
    #permission_classes = (IsAuthenticated,)

    def delete(self, request, pk=None, **kwargs):
        pass

    def get(self, request, pk=None, **kwargs):
        pass

    def patch(self, request, **kwargs):
        pass

    def post(self, request, **kwargs):
        #parser_classes = (FileUploadParser,)
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
            persisted_data_file_sub.file = request.FILES['file']
            persisted_data_file_sub.updated = timezone.now()
            persisted_data_file_sub.save()
            """
            try:
                persisted_data_file_sub.file = request.FILES['file']
                persisted_data_file_sub.updated = timezone.now()
                persisted_data_file_sub.save()
            except:
                #if we hit this, don't forget to set the state of *_sub to whatever's appropriate
                return Response(
                    {"message" : "Exception saving file upload"},
                    status = status.HTTP_400_BAD_REQUEST
                )            
            """
            return Response(
                {"message" : "all good, baby!"},
                status = status.HTTP_200_OK
            )
        else:
            return Response(
                data_file_sub_write_ser.errors,
                status = status.HTTP_400_BAD_REQUEST
            )