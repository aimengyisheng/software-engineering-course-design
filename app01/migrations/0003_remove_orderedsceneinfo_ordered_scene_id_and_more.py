# Generated by Django 4.0.5 on 2022-07-06 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_travelnewsinfo_news_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderedsceneinfo',
            name='ordered_scene_id',
        ),
        migrations.AddField(
            model_name='orderedsceneinfo',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
