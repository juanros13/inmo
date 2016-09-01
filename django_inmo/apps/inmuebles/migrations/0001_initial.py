# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-01 18:44
from __future__ import unicode_literals

import apps.inmuebles.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=450)),
                ('observaciones', models.TextField()),
                ('fecha_creacion', models.DateTimeField(editable=False)),
                ('fecha_modificacion', models.DateTimeField(editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Edificio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=450)),
                ('direccion', models.TextField()),
                ('imagen', sorl.thumbnail.fields.ImageField(blank=True, upload_to=apps.inmuebles.models.path_and_rename)),
                ('fecha_creacion', models.DateTimeField(editable=False)),
                ('fecha_modificacion', models.DateTimeField(editable=False)),
                ('administrador', models.ManyToManyField(blank=True, related_name='administradores', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Torre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=450)),
                ('fecha_creacion', models.DateTimeField(editable=False)),
                ('fecha_modificacion', models.DateTimeField(editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='UsuarioDepartamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('es_propietario', models.BooleanField(default=False)),
                ('es_habitante', models.BooleanField(default=False)),
                ('es_principal', models.BooleanField(default=False)),
                ('fecha_creacion', models.DateTimeField(editable=False)),
                ('fecha_modificacion', models.DateTimeField(editable=False)),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inmuebles.Departamento')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='departamento',
            name='edificio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inmuebles.Edificio'),
        ),
        migrations.AddField(
            model_name='departamento',
            name='torre',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='inmuebles.Torre'),
        ),
    ]
