# Generated by Django 3.0.7 on 2020-08-16 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_entry_nonce'),
    ]

    operations = [
        migrations.AddField(
            model_name='cards',
            name='title',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
