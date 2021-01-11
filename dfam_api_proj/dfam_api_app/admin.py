from django.contrib import admin

from .models import *

admin.site.register(DataFileType)
admin.site.register(DataFileEntity)
admin.site.register(DataFileEntityColumn)
admin.site.register(DataFileSubState)
admin.site.register(UserDataFileType)
