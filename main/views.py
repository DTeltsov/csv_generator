from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required


from .models import Schema, Column, DataSet
from .forms import (SchemaModelForm, ColumnFormsetEdit,
                    ColumnFormsetAdd, DatasetModelForm)
from .tasks import generate_csv


@login_required
def schemas(request):
    template_name = 'main/schemas.html'
    schemas = (Schema.objects
                     .filter(user=request.user)
                     .values('pk', 'title', 'date_modified'))
    return render(request, template_name, {'schemas': schemas})


@login_required
def create_schema(request):
    template_name = 'main/new_schema.html'
    if request.method == 'GET':
        schemaform = SchemaModelForm(request.GET or None)
        formset = ColumnFormsetAdd(queryset=Column.objects.none())
    elif request.method == 'POST':
        schemaform = SchemaModelForm(request.POST)
        formset = ColumnFormsetAdd(request.POST)
        if schemaform.is_valid() and formset.is_valid():
            schema = schemaform.save(commit=False)
            schema.user = request.user
            schema.save()
            for form in formset:
                column = form.save(commit=False)
                column.schema = schema
                column.save()
            return redirect(generate_dataset, pk=schema.pk)
    return render(request, template_name, {
        'schemaform': schemaform,
        'formset': formset,
    })


@login_required
def edit_schema(request, pk):
    template_name = 'main/edit_schema.html'
    schema = get_object_or_404(Schema, pk=pk, user=request.user)
    schemaform = SchemaModelForm(instance=schema)
    formset = ColumnFormsetEdit(
        queryset=(Column.objects.filter(schema_id=schema.pk))
    )
    if request.method == 'POST':
        schemaform = SchemaModelForm(request.POST, instance=schema)
        formset = ColumnFormsetEdit(request.POST)
        if schemaform.is_valid() and formset.is_valid():
            schema = schemaform.save(commit=False)
            schema.user = request.user
            schema.save()
            for form in formset:
                column = form.save(commit=False)
                column.schema_id = schema.pk
                column.save()
            return redirect(schemas)
        else:
            print(formset.errors)
    return render(request, template_name, {
        'schemaform': schemaform,
        'formset': formset,
    })


@login_required
def delete_schema(request, pk):
    schema = get_object_or_404(Schema, pk=pk, user=request.user)
    schema.delete()
    return redirect(schemas)


@login_required
def generate_dataset(request, pk):
    template_name = 'main/datasets.html'
    if request.method == 'GET':
        datasetform = DatasetModelForm(request.GET or None)
        datasets = (DataSet.objects
                           .filter(user=request.user, schema_id=pk)
                           .values('pk', 'date_created', 'state'))
    elif request.method == 'POST':
        datasetform = DatasetModelForm(request.POST)
        if datasetform.is_valid():
            dataset = datasetform.save(commit=False)
            dataset.user = request.user
            dataset.schema_id = pk
            dataset.save()
            generate_csv.delay(pk, dataset.rows_number, dataset.id)
            return redirect(generate_dataset, pk=pk)
    return render(request, template_name, {
        'datasetform': datasetform,
        'datasets': datasets,
    })


@login_required
def download_dataset(request, pk):
    dataset = DataSet.objects.get(pk=pk)
    file_path = dataset.file_path
    return redirect(file_path)


def signup(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(schemas)
    else:
        form = UserCreationForm()
    args['form'] = form
    return render(request, 'main/signup.html', args)