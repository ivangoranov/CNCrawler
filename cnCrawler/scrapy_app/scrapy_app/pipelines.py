# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pydoc import locate
import json

# useful for handling different item types with a single interface
import jsonschema

django_item = locate('main.models.ContractNotice')
with open('schema.json') as of:
    schema = json.load(of)

class SrapyAppPipeline(object):
    def process_item(self, item, spider):
        json_item = json.loads(str(item).replace("'", '"'))
        is_valid = jsonschema.validate(json_item, schema=schema)
        if is_valid:
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
