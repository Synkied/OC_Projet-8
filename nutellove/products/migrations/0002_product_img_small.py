# Generated by Django 2.0.3 on 2018-03-19 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='img_small',
            field=models.URLField(null=True),
        ),
    ]
