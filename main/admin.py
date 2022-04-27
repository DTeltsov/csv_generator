from django.contrib import admin
from .models import Column, ColumnType, DataSet, Schema

admin.site.register([Column, ColumnType, DataSet, Schema])
