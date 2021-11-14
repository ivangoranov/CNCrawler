# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pydoc import locate
import json

# useful for handling different item types with a single interface
django_item = locate('main.models.ContractNotice')


class SrapyAppPipeline(object):
    #def __init__(self, unique_id, *args, **kwargs):
    #    self.unique_id = unique_id
    #    self.items = []

    #@classmethod
    #def from_crawler(cls, crawler):
    #    return cls(
    #        unique_id=crawler.settings.get('unique_id'),  # this will be passed from django view
    #    )

    #def close_spider(self, spider):
    #    # And here we are saving our crawled data with django models.
    #    item = django_item()
    #    item.unique_id = self.unique_id
    #    item.data = json.dumps(self.items)

    def process_item(self, item, spider):
        try:
            contract_notice = django_item.objects.get(notice_number=item['notice_number'])
            print(f"Contract notice {item['notice_number']} already exist")
            return item
        except django_item.DoesNotExist:
            pass
        contract_notice = django_item()
        contract_notice.date = item['date']
        contract_notice.notice_number = item['notice_number']
        contract_notice.tender_name = item['tender_name']
        contract_notice.procedure_state = item['procedure_state']
        contract_notice.contract_type = item['contract_type']
        contract_notice.type_of_procurement = item['type_of_procurement']
        contract_notice.estimated_value = item['estimated_value']
        contract_notice.save()
        return item
