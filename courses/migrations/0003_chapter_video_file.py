# Generated by Django 5.1.2 on 2024-10-26 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_alter_category_options_alter_category_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='video_file',
            field=models.FileField(blank=True, upload_to='videos/'),
        ),
    ]