# Generated by Django 5.1.2 on 2024-12-18 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurance', '0002_alter_insuranceform_children_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insuranceform',
            name='income',
            field=models.IntegerField(),
        ),
    ]
