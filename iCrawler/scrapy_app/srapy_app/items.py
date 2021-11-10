# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem


import iCrawler
from ...main.models import *


class ContractNoticeScraperItem(DjangoItem):
    django_model = ContractNotice
    fields = ['date', 'notice_number', 'tender_name', 'procedure_state',
              'contract_type', 'type_of_procurement', 'estimated_value']
