# Generated by Django 5.1.2 on 2024-10-27 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_courseprogress_viewed_lessons'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='course_images/'),
        ),
    ]
