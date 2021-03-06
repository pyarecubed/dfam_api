"""dfam_api_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from dfam_api_app import views

urlpatterns = [
    path('admin/', admin.site.urls),    
    path('data_file_sub', views.DataFileSubView.as_view()),
    path('data_file_sub/meta_related', views.DataFileSubMetaRelatedView.as_view()),    
    path('data_file_sub_proc/data_file_subs', views.DataFileSubsView.as_view()),
    path('data_file_type_entities/<str:data_file_type>', views.DataFileTypeEntitiesView.as_view()),
    path('user/data_file_sub', views.UserDataFileSubView.as_view()),    
]
