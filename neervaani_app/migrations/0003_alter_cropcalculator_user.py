# Generated by Django 4.2 on 2024-12-07 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('neervaani_app', '0002_cropcalculator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cropcalculator',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='neervaani_app.user'),
        ),
    ]
