# Generated by Django 2.2.1 on 2019-06-04 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_auto_20190604_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(max_length=200, null=True, verbose_name='Адрес'),
        ),
    ]
