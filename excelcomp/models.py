from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Users(AbstractUser):
    level = models.SmallIntegerField(null=True)

    def __str__(self):
        return f'{self.id} - {self.username}'

class InsxCloudSupp(models.Model):
    issuerPolicyNumber = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=50)
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    middleName = models.CharField(max_length=200)
    uploadDate = models.DateField()
    dateSubmit = models.DateField()
    dateEffective = models.DateField()
    dateCancellation = models.DateField()
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=5)
    zipCode = models.IntegerField()
    country = models.CharField(max_length=50)
    phoneNumber = models.BigIntegerField()
    email = models.EmailField()
    lineOfCoverage = models.CharField(max_length=50)
    insuranceCompany = models.CharField(max_length=200)
    agencyName = models.CharField(max_length=100)
    broker = models.CharField(max_length=100)
    npn = models.BigIntegerField()
    transactionId = models.CharField(max_length=200, null=True)