# Generated by Django 4.2.1 on 2023-05-20 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0003_remove_travelnotes_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='travelnotes',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default='2023-05-20'),
            preserve_default=False,
        ),
    ]
