from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.utils import timezone


class Families(models.Model):
    leader = models.ForeignKey('People', on_delete=models.SET_NULL, related_name='leads_families', blank=True, null=True, db_column='leader_id')
    family_id = models.AutoField(primary_key=True)
    family_name = models.CharField(max_length=255)
    origin = models.TextField(blank=True, null=True)
    family_history = models.TextField(blank=True, null=True)
    important_events = models.TextField(blank=True, null=True)
    # family_tree_link = models.TextField(blank=True, null=True)
    family_img = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "families"
class CustomUser(AbstractBaseUser, PermissionsMixin):
    person = models.OneToOneField('People', on_delete=models.SET_NULL, null=True, related_name='user')

    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email



class People(models.Model):
    people = models.AutoField(primary_key=True, unique=True, db_column='person_id')
    family = models.ForeignKey(Families, on_delete=models.CASCADE, related_name='members', blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    full_name = models.CharField(max_length=255)
    full_name_vn = models.CharField(max_length=255, blank=True, null=True)
    gender = models.BooleanField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    contact_address = models.CharField(max_length=255, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    marital_status = models.CharField(max_length=50, blank=True, null=True)
    history = models.TextField(blank=True, null=True)
    achievement = models.TextField(blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    education_level = models.CharField(max_length=100, blank=True, null=True)
    health_status = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    death_date = models.DateField(blank=True, null=True)
    family_info = models.TextField(blank=True, null=True)
    profile_picture = models.CharField(max_length=255, default='/home/media/profile_pictures/default.png')
    hobbies_interests = models.TextField(blank=True, null=True)
    social_media_links = models.TextField(blank=True, null=True)
    cause_of_death = models.TextField(blank=True, null=True)
    place_of_birth = models.CharField(max_length=255, blank=True, null=True)
    place_of_death = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "people"

class Relationships(models.Model):
    relationship_id = models.AutoField(primary_key=True, db_column='relationship_id')
    person1 = models.ForeignKey(People, on_delete=models.CASCADE, related_name='person1_relationships')
    person2 = models.ForeignKey(People, on_delete=models.CASCADE, related_name='person2_relationships')
    relationship_type = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    relationship_img = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "relationships"
