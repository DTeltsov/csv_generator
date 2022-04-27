from django.urls import path
from django.views.generic import RedirectView
from .views import (schemas, create_schema, edit_schema,
                    delete_schema, generate_dataset, download_dataset)


urlpatterns = [
    path('', RedirectView.as_view(url='schemas/', permanent=True)),
    path('schemas/', schemas, name='schemas'),
    path('schemas/add', create_schema, name='new_schema'),
    path('schemas/edit/<pk>', edit_schema, name='edit_schema'),
    path('schemas/delete/<pk>', delete_schema, name='delete_schema'),
    path('schemas/datasets/<pk>', generate_dataset, name='datasets'),
    path('schemas/datasets/<pk>/download', download_dataset, name='download_dataset'),

]