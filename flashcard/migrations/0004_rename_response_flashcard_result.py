# Generated by Django 5.0.1 on 2024-01-17 23:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flashcard', '0003_rename_result_flashcard_response_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flashcard',
            old_name='response',
            new_name='result',
        ),
    ]
