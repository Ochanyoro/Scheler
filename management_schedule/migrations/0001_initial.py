# Generated by Django 3.1.6 on 2021-02-13 05:49

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserNickname',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=150, unique=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nickname', models.CharField(max_length=10, verbose_name='ニックネーム')),
                ('summary', models.CharField(max_length=50, verbose_name='概要')),
                ('description', models.TextField(blank=True, verbose_name='詳細な説明')),
                ('start_time', models.TimeField(default=datetime.time(7, 0), verbose_name='開始時間')),
                ('end_time', models.TimeField(default=datetime.time(7, 0), verbose_name='終了時間')),
                ('date', models.DateField(verbose_name='日付')),
                ('good_count', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='作成日')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management_schedule.group')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedule_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Good',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='good_owner', to=settings.AUTH_USER_MODEL)),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management_schedule.schedule')),
            ],
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management_schedule.group')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_owner', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='documents/%Y/%m/%d/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management_schedule.group')),
            ],
        ),
    ]
