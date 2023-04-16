# Generated by Django 4.2 on 2023-04-16 11:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'statuses',
            },
        ),
        migrations.CreateModel(
            name='Flashcard',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=2000)),
                ('description', models.CharField(max_length=2000)),
                ('hashtag', models.CharField(max_length=50)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bricabrac.category')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bricabrac.status')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
