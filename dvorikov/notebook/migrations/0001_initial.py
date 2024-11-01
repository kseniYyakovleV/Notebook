# Generated by Django 5.0.6 on 2024-10-30 05:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='New_model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='Название')),
                ('category', models.CharField(choices=[('d', 'Обычная'), ('i', 'Важная')], default='d', max_length=1, verbose_name='Категория')),
                ('start_datetime', models.DateTimeField(verbose_name='Время начала')),
                ('end_datetime', models.DateTimeField(verbose_name='Время конца')),
                ('task_description', models.TextField(verbose_name='Описание задачи')),
                ('is_periodic', models.BooleanField(verbose_name='Является периодической')),
                ('last_execution', models.DateTimeField(default=None, null=True, verbose_name='Последнее выполнение')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'unique_together': {('owner', 'title')},
            },
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period_duration', models.SmallIntegerField(verbose_name='Период повтора')),
                ('execution_duration', models.SmallIntegerField(verbose_name='Длительность выполнения')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notebook.task')),
            ],
        ),
    ]
