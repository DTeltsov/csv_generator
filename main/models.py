from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Schema(models.Model):
    class Separator(models.TextChoices):
        COMMA = ',', "Comma"
        SEMICOLON = ';', "Semicolon"
        PIPE = '|', "Pipe"

    class Character(models.TextChoices):
        QUOTES = "'", "Quotes"
        DOUBLE_QUOTES = '"', "Double quotes"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='schema',
    )
    title = models.CharField('Title', max_length=200)
    column_separator = models.CharField(
        'Separator',
        max_length=2,
        choices=Separator.choices,
        default=Separator.COMMA,
    )
    string_character = models.CharField(
        'Character',
        max_length=2,
        choices=Character.choices,
        default=Character.DOUBLE_QUOTES,
    )
    date_created = models.DateField('Creation date', auto_now_add=True)
    date_modified = models.DateField(
        'Modification date',
        auto_now=True
    )

    def __str__(self):
        return self.title


class ColumnType(models.Model):
    name = models.CharField('Name', max_length=200)
    has_range = models.BooleanField('Has range')

    def __str__(self):
        return self.name


class Column(models.Model):
    name = models.CharField('Name', max_length=200)
    schema = models.ForeignKey(
        Schema,
        on_delete=models.CASCADE,
        related_name='columns'
    )
    column_type = models.ForeignKey(
        ColumnType,
        on_delete=models.CASCADE,
        related_name='columns',
        null=True,
        blank=True,
    )
    range_from = models.IntegerField('Range from', blank=True, null=True)
    range_to = models.IntegerField('Range to', blank=True, null=True)
    column_number = models.IntegerField('Column number')

    def __str__(self):
        return self.name

    def clean(self):
        column_type = ColumnType.objects.get(pk=self.column_type.pk)
        if (column_type.has_range and
                (self.range_from is None or self.range_to is None)):
            raise ValidationError(
                {'range_from': "You must defiend range for this type"}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class DataSet(models.Model):
    class State(models.TextChoices):
        PROCESSING = 1, "Processing"
        READY = 2, "Ready"

    schema = models.ForeignKey(
        Schema,
        on_delete=models.CASCADE,
        related_name='datasets'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='dataset',
    )
    rows_number = models.IntegerField('Number of rows')
    state = models.CharField(
        'State',
        max_length=2,
        choices=State.choices,
        default=State.PROCESSING,
    )
    date_created = models.DateField('Creation date', auto_now=True)
    file_path = models.CharField(max_length=500, blank=True, null=True)
    file_name = models.CharField(max_length=500, blank=True, null=True)
