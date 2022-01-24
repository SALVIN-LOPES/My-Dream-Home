# Generated by Django 3.2.8 on 2021-12-22 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_auto_20211222_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='property_type',
            field=models.CharField(choices=[('1BHk', '1BHk'), ('2BHk', '2BHk'), ('3BHk', '3BHk'), ('4BHk', '4BHk')], default='1BHK', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='house',
            name='purpose',
            field=models.CharField(blank=True, choices=[('RENT', 'RENT'), ('SELL', 'SELL')], default='SELL', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='house',
            name='view',
            field=models.CharField(choices=[('Side_View', 'Side_View'), ('Front_View', 'Front_View'), ('Back_View', 'Back_View')], default='Side_View', max_length=200, null=True),
        ),
    ]