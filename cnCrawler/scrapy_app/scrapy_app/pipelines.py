# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pydoc import locate
import json
# useful for handling different item types with a single interface
import jsonschema

with open(f'./scrapy_app/scrapy_app/schema.json') as of:
    schema = json.load(of, strict=False)



django_item = locate('main.models.ContractNotice')



class SrapyAppPipeline(object):
        def process_item(self, item, spider):
            try:
                jsonschema.validate(json.loads(json.dumps(item._values)), schema=schema)
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
            except jsonschema.ValidationError as ve:
                print(ve.message)


