# Generated by Django 4.1.3 on 2022-11-30 08:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='comment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='blog.comment'),
            preserve_default=False,
        ),
    ]
