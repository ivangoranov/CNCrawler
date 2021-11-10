import os
from pydoc import locate

from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils import reactor
from scrapy.utils.project import get_project_settings



class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        settings_file_path = "scrapy_app.scrapy_app.settings"  # Scrapy Project Setting
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        settings = get_project_settings()
        spider = locate('scrapy_app.scrapy_app.spiders.cncrawler.ContractNoticesSpider')
        process = CrawlerProcess(settings)
        process.crawl(spider)
        process.start(stop_after_crawl=False)
        process.stop()