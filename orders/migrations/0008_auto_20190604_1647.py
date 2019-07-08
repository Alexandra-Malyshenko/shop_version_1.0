# Generated by Django 2.2.1 on 2019-06-04 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20190507_1817'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='last_name',
        ),
        migrations.AlterField(
            model_name='order',
            name='comments',
            field=models.TextField(blank=True, default='no comments', verbose_name='Комментарии'),
        ),
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='Email'),
        ),
    ]
