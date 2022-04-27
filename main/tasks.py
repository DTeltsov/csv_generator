from faker import Faker
from .models import Column, Schema, DataSet
from csv_generator.celery import app
import random
import csv
import boto3
from csv_generator.settings import (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, 
                                    AWS_STORAGE_BUCKET_NAME, AWS_URL)
import pandas as pd
from io import StringIO

fake = Faker()

s3_resource = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY)


def get_random_number(column_range):
    return random.randrange(column_range[0], column_range[1])


def get_text(column_range):
    text = fake.sentences(
        nb=random.randrange(column_range[0], column_range[1])
    )
    text = ' '.join(text)
    return text


def generate_rows(columns_dict):
    result = []
    for column_type, column_range in columns_dict.items():
        if column_type == 1:
            result.append(fake.name())
        elif column_type == 2:
            result.append(fake.job())
        elif column_type == 3:
            result.append(fake.email())
        elif column_type == 4:
            result.append(get_random_number(column_range))
        elif column_type == 5:
            result.append(get_text(column_range))
        elif column_type == 6:
            result.append(fake.company())
    return result


@app.task
def generate_csv(schema_pk, num_rows, dataset_pk):
    schema = Schema.objects.get(pk=schema_pk)
    columns = (
        Column.objects.filter(schema_id=schema_pk).order_by('column_number')
    )
    columns_dict = {}
    header = []
    for column in columns:
        columns_dict[column.column_type_id] = [column.range_from,
                                               column.range_to]
        header.append(column.column_type)
    df = pd.DataFrame(columns=header)
    title = '{0}_{1}.csv'.format(schema.title, num_rows)
    path = 'media/{0}/{1}'.format(str(dataset_pk), title)
    file_path = AWS_URL + path
    for _ in range(1, num_rows):
        df.loc[len(df)] = generate_rows(columns_dict)
    csv_buffer = StringIO()
    df.to_csv(
        csv_buffer,
        sep=schema.column_separator,
        quotechar=schema.string_character,
        quoting=csv.QUOTE_NONNUMERIC,
        index=False
    )
    (DataSet.objects
            .filter(pk=dataset_pk)
            .update(
                state=2, 
                file_path=file_path, file_name=title))
    s3_resource.Object(AWS_STORAGE_BUCKET_NAME, path).put(Body=csv_buffer.getvalue())

