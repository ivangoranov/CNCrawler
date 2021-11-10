from django.contrib import admin

from .models import ContractNotice
from .models import Profile

admin.site.register(ContractNotice)
admin.site.register(Profile)

