from django import forms
from django.forms import modelformset_factory, TextInput, Select, NumberInput

from .models import Column, Schema, DataSet


class SchemaModelForm(forms.ModelForm):
    class Meta:
        model = Schema
        fields = ('title', 'column_separator', 'string_character')
        labels = {
            'title': 'Title',
            'column_separator': 'Column separator',
            'string_character': 'String character'
        }
        widgets = {
            'title': TextInput(
                attrs={'class': "form-control", 'required': 'required'}
            ),
            'column_separator': Select(attrs={'class': 'form-select'}),
            'string_character': Select(attrs={'class': 'form-select'}),
        }


class DatasetModelForm(forms.ModelForm):
    class Meta:
        model = DataSet
        fields = ('rows_number',)
        labels = {
            'rows_number': 'Rows',
        }
        widgets = {
            'rows_number': NumberInput(
                attrs={'class': 'form-control', 'required': 'required'}
            ),
        }


ColumnFormsetAdd = modelformset_factory(
    Column,
    fields=('name', 'column_type', 'range_from', 'range_to', 'column_number'),
    extra=1,
    labels={
        'column_number': 'Order'
    },
    widgets={
        'name': TextInput(
            attrs={'class': 'form-control', 'required': 'required'}
        ),
        'column_type': Select(
            attrs={'class': 'form-select', 'required': 'required'}
        ),
        'range_from': NumberInput(attrs={'class': 'form-control'}),
        'range_to': NumberInput(attrs={'class': 'form-control'}),
        'column_number': NumberInput(
            attrs={'class': 'form-control', 'required': 'required'}
        )
    }
)

ColumnFormsetEdit = modelformset_factory(
    Column,
    fields=('name', 'column_type', 'range_from', 'range_to', 'column_number'),
    extra=0,
    labels={
        'column_number': 'Order'
    },
    widgets={
        'name': TextInput(
            attrs={'class': 'form-control', 'required': 'required'}
        ),
        'column_type': Select(
            attrs={'class': 'form-select', 'required': 'required'}
        ),
        'range_from': NumberInput(attrs={'class': 'form-control'}),
        'range_to': NumberInput(attrs={'class': 'form-control'}),
        'column_number': NumberInput(
            attrs={'class': 'form-control', 'required': 'required'}
        )
    }
)