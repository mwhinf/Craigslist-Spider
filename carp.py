import scrapydo
import logging
import os
import time
from CraigslistSpider.spiders import CraigSpider
from functionFile import emailFunc
from functionFile import buildBase
from functionFile import resetTables



scrapydo.setup()

duration = 60  # set up duration of crawl in minutes (multiples of 5)

timer = duration/5

os.environ['SCRAPY_SETTINGS_MODULE'] = 'CraigslistSpider.settings'

scrapydo.default_settings.update({
    'LOG_LEVEL': 'DEBUG',
    'CLOSESPIDER_PAGECOUNT': 10,
})

logging.basicConfig(level=logging.DEBUG)
logging.root.setLevel(logging.INFO)

base = scrapydo.run_spider(CraigSpider.LongboardsSpider, settings={'CLOSESPIDER_ITEMCOUNT': 500})

time.sleep(3)

#otherBase = scrapydo.run_spider(CraigSpider.LongboardsSpider, settings={'CLOSESPIDER_ITEMCOUNT': 500})

buildBase()

j=0

while j < timer:
    items = scrapydo.run_spider(CraigSpider.LongboardsSpider, settings={'CLOSESPIDER_ITEMCOUNT': 500})

    time.sleep(5)

    emailFunc()

    print('5 minutes')
    time.sleep(55)
    print('4 minutes')
    time.sleep(60)
    print('3 minutes')
    time.sleep(60)
    print('2 minutes')
    time.sleep(60)
    print('1 minute')
    time.sleep(60)

    j+=1


resetTables()




