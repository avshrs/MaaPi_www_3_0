# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from django.forms import ModelForm
from django.db import models
from maapi.choices import group


class Groups(models.Model):
    id = models.AutoField(primary_key=True)
    group0 = models.TextField(blank=True, null=True)
#    group1 = models.TextField(blank=True, null=True)
#    group2 = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'maapi_group'

