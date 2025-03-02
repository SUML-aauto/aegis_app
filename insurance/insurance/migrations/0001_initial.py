# Generated by Django 5.1.2 on 2024-10-24 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InsuranceForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=10)),
                ('age', models.IntegerField()),
                ('marital_status', models.CharField(choices=[('single', 'Single'), ('married', 'Married')], max_length=10)),
                ('children', models.IntegerField(blank=True, null=True)),
                ('income', models.CharField(max_length=100)),
                ('employment', models.CharField(choices=[('unemployed', 'Unemployed'), ('employed', 'Employed')], max_length=15)),
                ('disability', models.BooleanField(default=False)),
                ('make', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('fuel_type', models.CharField(max_length=20)),
                ('engine_power', models.IntegerField(blank=True, null=True)),
                ('body_type', models.CharField(max_length=50)),
                ('engine_volume', models.DecimalField(decimal_places=2, max_digits=5)),
                ('driving_experience', models.IntegerField()),
                ('vehicles_in_family', models.IntegerField()),
                ('accidents', models.IntegerField()),
                ('mileage', models.IntegerField()),
                ('vehicle_accidents', models.IntegerField()),
                ('market_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_owners', models.IntegerField()),
                ('dashcam', models.BooleanField(default=False)),
            ],
        ),
    ]
