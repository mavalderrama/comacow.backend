# Generated by Django 3.0.5 on 2020-04-04 00:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Farm',
            fields=[
                ('id_farm', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('n_cow', models.PositiveIntegerField()),
                ('n_bull', models.PositiveIntegerField()),
                ('n_calf', models.PositiveIntegerField()),
                ('lon', models.DecimalField(decimal_places=6, max_digits=9)),
                ('lat', models.DecimalField(decimal_places=6, max_digits=9)),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Livestock',
            fields=[
                ('id_animal', models.AutoField(primary_key=True, serialize=False)),
                ('chapeta', models.CharField(max_length=264)),
                ('animal_type', models.CharField(choices=[('CW', 'Cow'), ('BL', 'Bull'), ('CL', 'Calf')], max_length=2)),
                ('status', models.CharField(choices=[('FS', 'For Sale'), ('SD', 'Sold'), ('NA', 'Not Available')], max_length=2)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('raze', models.CharField(max_length=264)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('id_farm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Farm')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nit', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('pwd', models.CharField(max_length=500)),
                ('user_type', models.CharField(choices=[('FR', 'Farmer'), ('BC', 'Big Customer'), ('MM', 'Middle Man')], max_length=2)),
                ('phone', models.CharField(max_length=200)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MiddlemanOrder',
            fields=[
                ('id_order', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=264)),
                ('details', models.CharField(max_length=264)),
                ('id_animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Livestock')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FarmOrder',
            fields=[
                ('id_order', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('FS', 'For Sale'), ('SD', 'Sold'), ('NA', 'Not Available')], max_length=2)),
                ('details', models.CharField(max_length=500)),
                ('id_animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Livestock')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerOrder',
            fields=[
                ('id_order', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=264)),
                ('details', models.CharField(max_length=264)),
                ('id_animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Livestock')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]