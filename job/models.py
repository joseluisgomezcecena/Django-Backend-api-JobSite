from datetime import *

from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import Point

import geocoder
import os

# Create your models here.
class JobType(models.TextChoices):
    Permanent = 'Full time'
    PartTime = 'Part time'
    Internship = 'Internship'
    Freelance = 'Freelance'
    Temporary = 'Temporary'
    Contract = 'Contract'
    Volunteer = 'Volunteer'


class Education(models.TextChoices):
    Bachelors = 'Bachelors'
    Masters = 'Masters'
    Doctorate = 'Doctorate'
    PostDoctorate = 'Post Doctorate'


class Experience(models.TextChoices):
    NO_EXPERIENCE = 'No Experience'
    ONE_YEAR = '1 Year'
    TWO_YEARS = '2 Years'
    THREE_YEARS = '3 Years'
    FOUR_YEARS = '4 Years'
    FIVE_YEARS = '5 Years or more'



class Industry(models.TextChoices):
    Bussiness = 'Bussiness'
    Information_Technology = 'Information Technology'
    Education = 'Education'
    Health_Care = 'Health Care'
    Finance = 'Finance'
    Construction = 'Construction'
    Agriculture = 'Agriculture'
    Manufacturing = 'Manufacturing'
    Transportation = 'Transportation'
    Retail = 'Retail'
    Media = 'Media'
    Government = 'Government'
    Hospitality = 'Hospitality'
    Telecommunication = 'Telecommunication'
    Other = 'Other'


def return_date_time():
    now = datetime.now()
    return now + timedelta(days=30)


class Job(models.Model):
    title = models.CharField(max_length=100, null=True)
    description = models.TextField(max_length=1000, null=True)
    email = models.EmailField(null=True)
    address = models.CharField(max_length=100)
    job_type = models.CharField(
        max_length=100,
        choices=JobType.choices,
        default=JobType.Permanent,
    )

    education = models.CharField(
        max_length=100,
        choices=Education.choices,
        default=Education.Bachelors,
    )

    experience = models.CharField(
        max_length=100,
        choices=Experience.choices,
        default=Experience.NO_EXPERIENCE,
    )

    industry = models.CharField(
        max_length=100,
        choices=Industry.choices,
        default=Industry.Other,
    )

    salary = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(1000000)])
    positions = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(1000000)])
    company = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now=True)
    last_date = models.DateTimeField(default=return_date_time)
    point = gismodels.PointField(default=Point(0.0, 0.0), null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        g = geocoder.mapquest(self.address, key=os.environ.get('GEOCODER_API'))

        print(g)

        self.point = Point(g.lat, g.lng)
        super(Job, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
