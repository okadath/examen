# Generated by Django 4.2.14 on 2024-07-26 04:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='nombre',
            new_name='name',
        ),
    ]
