import datetime

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class ContractNotice(models.Model):
    date = models.DateTimeField()
    notice_number = models.CharField(max_length=50)
    tender_name = models.CharField(max_length=2083, null=True, blank=True)
    procedure_state = models.CharField(max_length=50, null=True, blank=True)
    contract_type = models.CharField(max_length=50, null=True, blank=True)
    type_of_procurement = models.CharField(max_length=50)
    estimated_value = models.DecimalField(max_digits=19, decimal_places=2)

    # noinspection PyUnresolvedReferences
    def __str__(self):
        return f"{self.date} {self.notice_number}"

    # noinspection PyUnresolvedReferences
    def __unicode__(self):
        return f"{datetime.strftime(str(self.date))} {self.notice_number}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()

    # noinspection PyUnresolvedReferences
    def __str__(self):
        return f'{self.user.username} Profile'
