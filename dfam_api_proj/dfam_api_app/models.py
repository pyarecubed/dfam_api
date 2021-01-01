from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.validators import MinValueValidator
from django.db import models

from rest_framework.authentication import TokenAuthentication

import os

"""
TODO be wise to craft some fixtures to initialize things - expecially our enumish models
"""

dfs_fs = FileSystemStorage(location = settings.UPLOAD_PATH)

def data_file_sub_upload_to(instance, post_filename):
    file_ext = os.path.splitext(post_filename)[-1]
    file_name = "{0}{1}".format(
        instance.uuid,
        file_ext
    )
    return os.path.join(
        settings.UPLOAD_PATH,
        file_name
    )

class DataFileType(models.Model):
    """
    Enumeration of the formats/types of data files that can be uploaded
    """
    name = models.CharField(
        max_length = 100,
        null = False,
        unique = True,
        blank = False
    )

    display_name = models.CharField(
        max_length = 100,
        null = False,
        blank = False
    )

    description = models.CharField(
        max_length = 255,
        null = True,
        blank = True
    )

    def __str__(self):
        return "DataFileType: {0}".format(self.display_name)

    class Meta:
        verbose_name = "Data File Type"
        verbose_name_plural = "Data File Types"

class DataFileEntity(models.Model):
    """
    Enumeration of the entities represented within a row of a given DataFileType
    """
    data_file_type = models.ForeignKey(
        DataFileType,
        on_delete = models.CASCADE,
        related_name = "entity"    
    )

    name = models.CharField(
        max_length = 100,
        null = False,
        blank = False
    )

    display_name = models.CharField(
        max_length = 100,
        null = False,
        blank = False
    )    

    description = models.CharField(
        max_length = 255,
        null = True,
        blank = True
    )

    def __str__(self):
        return "DataFileEntity: {0} of {1}".format(
            self.display_name,
            str(self.data_file_type)
        )

    class Meta:
        verbose_name = "Data File (row) Entity"
        verbose_name_plural = "Data File (row) Entities"
        constraints = [
            models.UniqueConstraint(
                fields = ["data_file_type", "name"],
                name = "dfe_dft_n"
            )
        ]

class DataFileEntityColumn(models.Model):
    """
    Enumeration of the columns within a given DataFileType that constitute a given DataFileEntity
    """
    data_file_entity = models.ForeignKey(
        DataFileEntity,
        on_delete = models.CASCADE,
        related_name = "col"
    )

    name = models.CharField(
        max_length = 100,
        null = False,
        blank = False
    )

    display_name = models.CharField(
        max_length = 100,
        null = False,
        blank = False
    )

    col_name = models.CharField(
        max_length = 255,
        null = False,
        blank = False
    )

    description = models.CharField(
        max_length = 255,
        null = True,
        blank = True
    )

    def __str__(self):
        return "DataFileEntityColumn: {0} of {1}".format(
            self.display_name,
            str(self.data_file_entity)
        )

    class Meta:
        verbose_name = "Data File (row) Entity Column"
        verbose_name_plural = "Data File (row) Entity Columns"
        constraints = [
            models.UniqueConstraint(
                fields = ["data_file_entity", "name", "column_name"],
                name = "dfec_dfe_n_cn"
            )
        ]

class UserDataFileType(models.Model):
    """
    Association of (Django Auth) Users to Data File Type(s) 
    """
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = "user_data_file_type"
    )

    data_file_type = models.ForeignKey(
        DataFileType,
        on_delete = models.CASCADE,
        related_name = "data_file_type_user"
    )

    def __str__(self):
        return "User: {0} ({1} {2}) <-> {3}".format(
            self.user.username,
            self.user.first_name,
            self.user.last_name,
            str(self.data_file_type)
        )

    class Meta:
        verbose_name = "User <-> Data File Type"
        verbose_name_plural = "User(s) <-> Data File Type(s)"
        constraints = [
            models.UniqueConstraint(
                fields = ["user", "data_file_type"],
                name = "udft_u_dft"
            )
        ]

class DataFileSubState(models.Model):
    """
    Enumeration of Data File Submission (processing) States
    """
    name = models.CharField(
        max_length = 100,
        null = False,
        unique = True,
        blank = False
    )

    display_name = models.CharField(
        max_length = 100,
        null = False,
        blank = False
    )

    def __str__(self):
        return "DataFileSubState: {0}".format(
            self.display_name
        )

    class Meta:
        verbose_name = "Data File Submission State"
        verbose_name_plural = "Data File submission States"

class DataFileSub(models.Model):
    """
    Uploaded/Submitted Data Files
    """
    uuid = models.CharField(
        max_length = 36,
        null = False,
        blank = False,
        unique = True
    )

    file = models.FileField(
        storage = dfs_fs,
        upload_to = data_file_sub_upload_to,
        null = False,
        blank = False
    )

    data_file_type = models.ForeignKey(
        DataFileType,
        on_delete = models.CASCADE,
        related_name = "data_file_type_sub",
        null = True,
        blank = True
    )

    data_file_sub_state = models.ForeignKey(
        DataFileSubState,
        on_delete = models.CASCADE,
        related_name = "data_file_state_sub",
        null = True,
        blank = True
    )

    data_file_sub_state_description = models.CharField(
        max_length = 255,
        null = True,
        blank = True
    )

    owner = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = "owned_data_file_state_sub"
    )

    submitter = models.CharField(
        max_length = 255,
        null = False,
        blank = False
    )

    submitted = models.DateTimeField(
        auto_now = True,
        null = False,
        blank = False
    )

    updated = models.DateTimeField(
        null = False,
        blank = False
    )

    def __str__(self):
        return "{0}'s DataFileSub: {1} of {2} in {3}".format(
            self.file_name,
            str(self.data_file_type),
            str(self.data_file_sub_state)
        )

    class Meta:
        verbose_name = "Data File Submission"
        verbose_name_plural = "Data File Submissions"

class DataFileSubEntity(models.Model):
    """
    Expression of entities found in a given submission
    """
    data_file_sub = models.ForeignKey(
        DataFileSub,
        on_delete = models.CASCADE,
        related_name = "entity"
    )

    data_file_entity = models.ForeignKey(
        DataFileEntity,
        on_delete = models.CASCADE
    )

    novel = models.BooleanField(
        default = False
    )

    def __str__(self):
        return "{0} of {1}".format(
            str(self.data_file_entity),
            str(self.data_file_sub)
        )

    class Meta:
        verbose_name = "Data File Submission Entity"
        verbose_name_plural = "Data File Submission Entities"
        constraints = [
            models.UniqueConstraint(
                fields = ["data_file_sub", "data_file_entity"],
                name = "dfse_dfs_dfe"
            )
        ]

class DataFileSubEntityColVal(models.Model):
    """
    Expression of the entity, column and observed value from a submitted file
    """
    data_file_sub_entity = models.ForeignKey(
        DataFileSubEntity,
        on_delete = models.CASCADE,
        related_name = "col_val"
    )

    data_file_entity_column = models.ForeignKey(
        DataFileEntityColumn,
        on_delete = models.CASCADE        
    )

    col_value = models.CharField(
        max_length = 255,
        null = False,
        blank = False
    )

    def __str__(self):
        return "{0} = {1} for {2}".format(
            str(self.data_file_entity_column),
            str(self.col_value),
            str(self.data_file_sub_entity)
        )

    class Meta:
        verbose_name = "Data File Submission Entity Column Value"
        verbose_name_plural = "Data File Submission Entity Column Values"
        constraints = [
            models.UniqueConstraint(
                fields = ["data_file_sub_entity", "data_file_entity_column"],
                name = "dfsecv_dfse_dfec"
            )
        ]

class DataFileSubEntityLine(models.Model):
    """
    Expression of the line numbers where an entity was found in a submitted file
    """
    data_file_sub_entity = models.ForeignKey(
        DataFileSubEntity,
        on_delete = models.CASCADE,
        related_name = "line_col_val"
    )

    line_number = models.PositiveIntegerField(
        null = False,
        blank = False,
        validators = [MinValueValidator(1)]
    )

    def __str__(self):
        return "{0} found in line {1}".format(
            str(data_file_sub_entity),
            str(self.line_number)
        )

    class Meta:
        verbose_name = "Data File Submission Entity Line"
        verbose_name_plural = "Data File Submission Entity Lines"
        constraints = [
            models.UniqueConstraint(
                fields = ["data_file_sub_entity", "line_number"],
                name = "dfsel_dfse_ln"
            )
        ]

class RemoteSetEntity(models.Model):
    """
    Expression of entity from a remote object set that we're attempting to match against
    (might be a crazy idea, but we might want to populate this exhaustively)
    """
    data_file_sub = models.ForeignKey(
        DataFileSub,
        on_delete = models.CASCADE,
        related_name = "matching_set_entity"
    )

    data_file_entity = models.ForeignKey(
        DataFileEntity,
        on_delete = models.CASCADE
    )

    remote_key = models.CharField(
        max_length = 100,
        null = False,
        blank = False
    )

    def __str__(self):
        return "Remote entity({0}) for {1}, {2}".format(
            self.remote_key,
            str(self.data_file_sub),
            str(self.data_file_entity)
        )
    
    class Meta:
        verbose_name = "Remote Set Entity"
        verbose_name_plural = "Remote Set Entities"
        constraints = [
            models.UniqueConstraint(
                fields = ["data_file_sub", "data_file_entity"],
                name = "rse_dfs_dfe"
            )
        ]

class RemoteSetEntityColVal(models.Model):
    """
    Expression of a remote set entity, column and value
    """
    remote_set_entity = models.ForeignKey(
        RemoteSetEntity,
        on_delete = models.CASCADE,
        related_name = "col_val"
    )

    data_file_entity_column = models.ForeignKey(
        DataFileEntityColumn,
        on_delete = models.CASCADE        
    )

    col_value = models.CharField(
        max_length = 255,
        null = False,
        blank = False
    )

    def __str__(self):
        return "{0} = {1} for {2}".format(
            str(self.data_file_entity_column),
            str(self.col_value),
            str(self.remote_set_entity)
        )

    class Meta:
        verbose_name = "Remote Set Entity Column Value"
        verbose_name_plural = "Remote set Entity Column Values"
        constraints = [
            models.UniqueConstraint(
                fields = ["remote_set_entity", "data_file_entity_column"],
                name = "rsecv_dfse_dfec"
            )
        ]

class DataFileSubEntityRemoteSetEntityAutoMatch(models.Model):
    data_file_entity = models.ForeignKey(
        DataFileEntity,
        on_delete = models.CASCADE,
        related_name = "auto_match"
    )

    remote_set_entity = models.ForeignKey(
        RemoteSetEntity,
        on_delete = models.CASCADE     
    )

    match_score = models.PositiveIntegerField(
        null = False,
        blank = False
    )

    def __str__(self):
        return "{0} <-({1})-> {1}".format(
            str(self.data_file_entity),
            str(self.match_score),
            str(self.remote_set_entity)
        )

    class Meta:
        verbose_name = "Data File Submission Entity Remote Set Entity Auto Match"
        verbose_name_plural = "Data File Submission Entity Remote Set Entity Auto Matches"
        constraints = [
            models.UniqueConstraint(
                fields = ["data_file_entity", "remote_set_entity"],
                name = "dfserseam_dfe_rse"
            )
        ]

class DataFileSubEntityRemoteSetEntityEquiv(models.Model):
    data_file_entity = models.ForeignKey(
        DataFileEntity,
        on_delete = models.CASCADE,
        related_name = "equiv"
    )

    remote_set_entity = models.ForeignKey(
        RemoteSetEntity,
        on_delete = models.CASCADE     
    )

    class Meta:
        verbose_name = "Data File Submission Entity Remote Set Entity Equivalent"
        verbose_name_plural = "Data File Submission Entity Remote Set Entity Equivalents"
        constraints = [
            models.UniqueConstraint(
                fields = ["data_file_entity", "remote_set_entity"],
                name = "dfsersee_dfe_rse"
            )
        ]

class DRFBearerAuth(TokenAuthentication):
    keyword = "Bearer"