from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.utils import timezone
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    def __str__(self):
        return self.email



class Families(models.Model):
    family_id = models.AutoField(primary_key=True)
    leader = models.IntegerField(null=True)
    # person = models.ForeignKey(People, on_delete=models.CASCADE, related_name='person_families')
    # Families table is one to many with People table
    family_name = models.CharField(max_length=255)
    origin = models.TextField(null=True)
    family_history = models.TextField(null=True)
    important_events = models.TextField(null=True)
    family_tree_link = models.TextField(null=True)
    family_img = models.CharField(max_length=255, null=True)
    class Meta:
        db_table = "families"
class People(models.Model):
    email = models.EmailField(_("email address"), unique=True, null=True)
    people_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    full_name_vn = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    gender = models.BooleanField(null=True)
    phone_number = models.CharField(max_length=20, null=True)
    contact_address = models.CharField(max_length=255, null=True)
    nationality = models.CharField(max_length=50, default='Việt Nam', null=True)
    birth_place = models.CharField(max_length=255, null=True)
    marital_status = models.CharField(max_length=50, null=True)
    history = models.TextField(null=True)
    achievement = models.TextField(null=True)
    occupation = models.CharField(max_length=100, null=True)
    education_level = models.CharField(max_length=100, null=True)
    health_status = models.CharField(max_length=255, null=True)
    death_date = models.DateField(null=True, blank=True)
    family_info = models.TextField(null=True)
    profile_picture = models.CharField(max_length=255, null=True)  # Modified field
    hobbies_interests = models.TextField(null=True)
    social_media_links = models.TextField(null=True)
    cause_of_death = models.TextField(null=True)
    family = models.ForeignKey('families', on_delete=models.CASCADE, related_name='people_families', null=True)
    
    class Meta:
        db_table = "people"
class Relationships(models.Model):
    relationship_id = models.AutoField(primary_key=True)
    person1 = models.ForeignKey(People, on_delete=models.CASCADE, related_name='person1_relationships')
    person2 = models.ForeignKey(People, on_delete=models.CASCADE, related_name='person2_relationships')
    relationship_type = models.CharField(max_length=100)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True, blank=True)
    relationship_img = models.CharField(max_length=255, null=True)
    class Meta:
        db_table = "relationships"