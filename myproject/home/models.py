from django.db import models

class People(models.Model):
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
    profile_picture = models.TextField(null=True)
    hobbies_interests = models.TextField(null=True)
    social_media_links = models.TextField(null=True)

    def __str__(self):
        return self.full_name
