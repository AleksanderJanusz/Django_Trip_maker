# Generated by Django 4.2.1 on 2023-05-27 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0003_alter_travel_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travelnotes',
            name='status',
            field=models.IntegerField(choices=[(0, 'Przed podróżą'), (1, 'W trakcie podróży'), (2, 'Po podróży')], default=0),
        ),
    ]
