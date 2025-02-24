# Generated by Django 5.1.6 on 2025-02-24 12:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0002_remove_moduleinstance_professor_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="module",
            name="module_code",
            field=models.CharField(max_length=5, unique=True),
        ),
        migrations.AlterField(
            model_name="professor",
            name="professor_code",
            field=models.CharField(max_length=5, unique=True),
        ),
    ]
