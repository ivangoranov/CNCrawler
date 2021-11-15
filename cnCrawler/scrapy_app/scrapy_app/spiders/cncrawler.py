import scrapy
import json
from pydoc import locate
from datetime import datetime, date
from scrapy import Request

scraped_item = locate('scrapy_app.scrapy_app.items.ContractNoticeScrapyItem')


class ContractNoticesSpider(scrapy.Spider):
    name = "cncrawler"

    def start_requests(self):
        today = datetime.now().date()
        url = 'http://www.e-licitatie.ro/api-pub/NoticeCommon/GetCNoticeList/'

        headers = {
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "RefreshToken": "null",
            "Authorization": "Bearer null",
            "Culture": "en-US",
            "HttpSessionID": "null",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
            "Content-Type": "application/json;charset=UTF-8",
            "Sec-GPC": "1",
            "Origin": "http://www.e-licitatie.ro",
            "Referer": "http://www.e-licitatie.ro/pub/notices/contract-notices/list/2/1",
            "Accept-Language": "en-US,en;q=0.9"
        }

        cookies = {
            "_HttpSessionID": "448ADF8A76B84F158292249DB4CFE471",
            "isCompact": "true",
            "culture": "en-US",
            "nutsIds": "%5B%5D",
            "sysNoticeTypeIds": "null",
            "selectedSysProcedureState": "null"
        }

        body = {"sysNoticeTypeIds": [2], "sortProperties": [], "pageSize": 1000, "hasUnansweredQuestions": 'false',
                "startPublicationDate": f"{today}T11:00:00.000Z",
                "startTenderReceiptDeadline": f"{today}T00:00:00.000Z",
                "sysProcedureStateId": 2, "pageIndex": 0}

        request = Request(
            url=url,
            method='POST',
            dont_filter=True,
            cookies=cookies,
            headers=headers,
            body=str(body),
        )

        yield request

    def parse(self, response, **kwargs):
        json_response = json.loads(response.text)
        items = scraped_item()
        for item in json_response['items']:
            items['date'] = str(datetime.strptime(item['noticeStateDate'].split('T')[0].replace('-', ':'),
                                                  '%Y:%m:%d').date())
            items['notice_number'] = item['noticeNo']
            items['tender_name'] = item['contractTitle']
            items['procedure_state'] = item['sysProcedureState']['text']
            items['contract_type'] = item['sysAcquisitionContractType']['text']
            items['type_of_procurement'] = 'ONLINE' if item['isOnline'] else 'OFFLINE'
            items['estimated_value'] = item['estimatedValueRon']

            yield items
