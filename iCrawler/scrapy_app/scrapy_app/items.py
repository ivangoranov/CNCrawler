# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from pydoc import locate


class ContractNoticeDjangoItem(DjangoItem):
    django_model = locate('main.models.ContractNotice')
    fields = ['date', 'notice_number', 'tender_name', 'procedure_state',
              'contract_type', 'type_of_procurement', 'estimated_value']


class ContractNoticeScrapyItem(scrapy.Item):
    date = scrapy.Field()
    notice_number = scrapy.Field()
    tender_name = scrapy.Field()
    procedure_state = scrapy.Field()
    contract_type = scrapy.Field()
    type_of_procurement = scrapy.Field()
    estimated_value = scrapy.Field()