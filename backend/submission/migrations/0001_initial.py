# Generated by Django 4.2.23 on 2025-07-16 19:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('problems', '0009_alter_problem_p_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CodeSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('python', 'Python'), ('java', 'Java'), ('cpp', 'C++'), ('c', 'C')], max_length=10)),
                ('code', models.TextField()),
                ('input_data', models.TextField(blank=True, null=True)),
                ('output', models.TextField(blank=True, null=True)),
                ('verdict', models.CharField(choices=[('AC', 'Accepted'), ('WA', 'Wrong Answer'), ('TLE', 'Time Limit Exceeded'), ('CE', 'Compilation Error'), ('RE', 'Runtime Error')], max_length=3)),
                ('score', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problems.problem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
