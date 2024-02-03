# Generated by Django 5.0.1 on 2024-02-03 11:07

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='People',
            fields=[
                ('people_id', models.AutoField(primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=255)),
                ('full_name_vn', models.CharField(max_length=255)),
                ('birth_date', models.DateField()),
                ('gender', models.BooleanField()),
                ('phone_number', models.CharField(max_length=20, null=True)),
                ('contact_address', models.CharField(max_length=255, null=True)),
                ('nationality', models.CharField(default='Việt Nam', max_length=50)),
                ('birth_place', models.CharField(max_length=255, null=True)),
                ('marital_status', models.CharField(max_length=50, null=True)),
                ('history', models.TextField(null=True)),
                ('achievement', models.TextField(null=True)),
                ('occupation', models.CharField(max_length=100, null=True)),
                ('education_level', models.CharField(max_length=100, null=True)),
                ('health_status', models.CharField(max_length=255, null=True)),
                ('death_date', models.DateField(blank=True, null=True)),
                ('family_info', models.TextField(null=True)),
                ('profile_picture', models.CharField(max_length=255, null=True)),
                ('hobbies_interests', models.TextField(null=True)),
                ('social_media_links', models.TextField(null=True)),
            ],
            options={
                'verbose_name': 'People',
                'db_table': 'People',
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Families',
            fields=[
                ('family_id', models.AutoField(primary_key=True, serialize=False)),
                ('family_name', models.CharField(max_length=255)),
                ('origin', models.TextField()),
                ('family_history', models.TextField()),
                ('important_events', models.TextField()),
                ('family_tree_link', models.TextField()),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person_families', to='home.people')),
            ],
            options={
                'verbose_name': 'Families',
                'db_table': 'Families',
            },
        ),
        migrations.CreateModel(
            name='Relationships',
            fields=[
                ('relationship_id', models.AutoField(primary_key=True, serialize=False)),
                ('relationship_type', models.CharField(max_length=100)),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('person1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person1_relationships', to='home.people')),
                ('person2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person2_relationships', to='home.people')),
            ],
            options={
                'verbose_name': 'Relationships',
                'db_table': 'Relationships',
            },
        ),
    ]
