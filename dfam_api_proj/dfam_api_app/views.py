from django.http import Http404
from django.shortcuts import render

from rest_framework import filters, generics, status
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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