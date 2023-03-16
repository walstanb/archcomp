# Generated by Django 4.1.7 on 2023-03-15 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archcomp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfile',
            name='folderpath',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='uploadedfile',
            name='uuid',
            field=models.UUIDField(editable=False, primary_key=True, serialize=False),
        ),
    ]
