# Generated by Django 4.1.1 on 2022-09-19 23:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_remove_comment_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='content',
            new_name='answer',
        ),
    ]
