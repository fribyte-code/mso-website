# Generated by Django 5.0.9 on 2024-10-10 17:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_homepage_body_homepage_hero_cta_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepage',
            name='hero_cta',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='hero_cta_link',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='image',
        ),
    ]
