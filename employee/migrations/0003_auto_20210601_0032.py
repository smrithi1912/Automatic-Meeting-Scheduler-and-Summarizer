# Generated by Django 3.1.4 on 2021-05-31 19:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_meeting'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting',
            name='summary',
        ),
        migrations.AddField(
            model_name='meeting',
            name='summary',
            field=models.TextField(blank=True),
        ),
        migrations.CreateModel(
            name='Meets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.employee')),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.meeting')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='meetings',
            field=models.ManyToManyField(through='employee.Meets', to='employee.meeting'),
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='participants',

        ),
        migrations.AddField(
            model_name='meeting',
            name='participants',
            field=models.ManyToManyField(through='employee.Meets', to='employee.employee'),
        ),
    ]
