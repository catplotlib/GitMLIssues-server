# Generated by Django 4.2.2 on 2023-06-21 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='name',
            new_name='lang',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='owner',
            new_name='repository',
        ),
        migrations.RemoveField(
            model_name='issue',
            name='description',
        ),
        migrations.RemoveField(
            model_name='issue',
            name='number',
        ),
        migrations.RemoveField(
            model_name='issue',
            name='project',
        ),
        migrations.RemoveField(
            model_name='project',
            name='type',
        ),
        migrations.AddField(
            model_name='issue',
            name='owner',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='issue',
            name='repository',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='project',
            name='desc',
            field=models.CharField(default='', max_length=400),
        ),
    ]