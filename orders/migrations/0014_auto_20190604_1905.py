# Generated by Django 2.2.1 on 2019-06-04 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_auto_20190604_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(blank=True, default='email@email.com', max_length=254, null=True, verbose_name='Email'),
        ),
    ]
