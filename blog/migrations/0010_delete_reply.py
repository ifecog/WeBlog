# Generated by Django 4.1.3 on 2022-11-30 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_view_remove_post_views'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Reply',
        ),
    ]
