from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email + " " + self.username


class People(models.Model):
    people_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255, null=True)
    birth_date = models.DateField(null=True)
    gender = models.CharField(max_length=50, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    contact_address = models.CharField(max_length=255, null=True)
    nationality = models.CharField(max_length=50, null=True)
    birth_place = models.CharField(max_length=255, null=True)
    marital_status = models.CharField(max_length=50, null=True)
    history = models.TextField(null=True)
    achievement = models.TextField(null=True)
    occupation = models.CharField(max_length=100, null=True)
    education_level = models.CharField(max_length=100, null=True)
    health_status = models.CharField(max_length=255, null=True)
    death_date = models.DateField(null=True, blank=True)
    family_info = models.TextField(null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True)  # Modified field
    hobbies_interests = models.TextField(null=True)
    social_media_links = models.TextField(null=True)

    def __str__(self):
        return self.full_name

class Relationships(models.Model):
    relationship_id = models.AutoField(primary_key=True)
    person1 = models.OneToOneField(People, on_delete=models.CASCADE, related_name='person1_relationships')
    person2 = models.OneToOneField(People, on_delete=models.CASCADE, related_name='person2_relationships')
    relationship_type = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

class Families(models.Model):
    family_id = models.AutoField(primary_key=True)
    person = models.ForeignKey(People, on_delete=models.CASCADE, related_name='person_families')
    # Families table is one to many with People table
    family_name = models.CharField(max_length=255)
    origin = models.TextField()
    family_history = models.TextField()
    important_events = models.TextField()
    family_tree_link = models.TextField()