# Generated by Django 5.1.2 on 2024-10-26 08:17

import embed_video.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_chapter_video_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='video_url',
            field=embed_video.fields.EmbedVideoField(blank=True),
        ),
    ]