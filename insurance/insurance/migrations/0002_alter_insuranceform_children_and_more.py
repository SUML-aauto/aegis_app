# Generated by Django 5.1.2 on 2024-11-06 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insuranceform',
            name='children',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='insuranceform',
            name='employment',
            field=models.CharField(choices=[('unemployed', 'Unemployed'), ('employed', 'Employed')], default='unemployed', max_length=15),
        ),
        migrations.AlterField(
            model_name='insuranceform',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female')], default='male', max_length=10),
        ),
        migrations.AlterField(
            model_name='insuranceform',
            name='marital_status',
            field=models.CharField(choices=[('single', 'Single'), ('married', 'Married')], default='single', max_length=10),
        ),
    ]
