from django.contrib.auth.models import User
from django.db import models

"""
TODO be wise to craft some fixtures to initialize things - expecially our enumish models
"""

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
                name = "datafileentity_dft_n"
            )
        ]

class DataFileEntityColumn(models.Model):
    """
    Enumeration of the columns within a given DataFileType that constitute a given DataFileEntity
    """
    data_file_entity = models.ForeignKey(
        DataFileEntity,
        on_delete = models.CASCADE,
        related_name = "column"
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

    column_name = models.CharField(
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
                name = "datafileentitiycolumn_dfe_n_cn"
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
        DataFileEntity,
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
                name = "userdatafiletype_u_dft"
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
        max_length = 32,
        min_length = 32,
        null = False,
        blank = False,
        unique = True
    )

    file_name = models.CharField(
        max_length = 40
        null = False,
        blank = False,
        unique = True
    )

    data_file_type = models.ForeignKey(
        DataFileType,
        on_delete = models.CASCADE,
        related_name = "data_file_type_sub"
    )

    data_file_sub_state = models.ForeignKey(
        DataFileSubState,
        on_delete = models.CASCADE,
        related_name = "data_file_state_sub"
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