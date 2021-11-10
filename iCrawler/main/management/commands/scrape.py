import os
from pydoc import locate

from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerRunner
from scrapy.utils import reactor
from scrapy.utils.project import get_project_settings


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        #print('trying to start the spider')
        #os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'contract_notices_scraper.data_collection.settings')
        #process = CrawlerProcess(get_project_settings())
        #process.crawl(ContractNoticesSpider)
        #process.start()
        settings_file_path = "contract_notices.data_collection.settings"  # Scrapy Project Setting
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        settings = get_project_settings()
        runner = CrawlerRunner(settings)

        path = "contract_notices.data_collection.spiders.contract_notices_spider"
        file_path = ".SampleSpider".format(path)

        SampleSpider = locate(file_path)

        d = runner.crawl(SampleSpider)
        d.addBoth(lambda _: reactor.stop())
        reactor.run()