from CraigslistSpider.items import CustomSpider
import scrapy
import datetime
import hashlib
import pytz
import re


MY_ADDRESS = 'pythonmail310@gmail.com'
PASSWORD = 'pythonmail'

# set current date and time
today = datetime.datetime.now(pytz.utc) - datetime.timedelta(hours=7)


class LongboardsSpider(scrapy.Spider):

    name = 'bear'
    allowed_domains = ['craigslist.org']

    def __init__(self, *args, **kwargs):
        super(LongboardsSpider, self).__init__(*args, **kwargs)

        self.start_urls = [kwargs.get('start_url')]

    def parse(self, response):
        global message
        boards = response.xpath('//p[@class="result-info"]')

        print('WOOOOO')
        print(self.start_urls)
        print('WOOOO')

        k = 1

        for board in boards:
            relative_url = board.xpath('a/@href').extract_first()
            absolute_url = response.urljoin(relative_url)
            title = board.xpath('a/text()').extract_first()
            location = board.xpath(
                'span[@class="result-meta"]/span[@class="result-hood"]/text()').extract_first("")[2:-1]
            postDate = board.xpath('time[@class="result-date"]/text()').extract_first("")
            price = board.xpath(
                'span[@class="result-meta"]/span[@class="result-price"]/text()').extract_first("")

            tempString = postDate   # format date string
            cutString = re.sub(r'  ', r' ', tempString)

            if cutString == today.strftime('%b %-d'):
                boardObject = {'title': title, 'postDate': postDate,
                               'price': price, 'URL': absolute_url, 'location': location}

                yield scrapy.Request(absolute_url, callback=self.parse_page, priority=k, meta={'passedObject': boardObject})
                k += 1

    def parse_page(self, response):
        img = response.xpath('//div[@class="slide first visible"]/img/@src')
        boardObject = response.meta['passedObject']
        imageURL = img.extract_first()
        print(imageURL)
        hashedURL = imageURL.encode('utf-8')
        hashBytes = hashlib.sha1(hashedURL)
        imgHash = hashBytes.hexdigest()
        imgHash += ".jpg"

        message = '\n' + '\n' + boardObject['price'] + '<br>' + '\n' + 'Date Posted: ' + boardObject['postDate'] + '<br>' + \
            '\n' + boardObject['title'] + '<br>' + '\n' + \
            boardObject['URL'] + '<br>' + '\n' + boardObject['location']

        yield CustomSpider(image_urls=[imageURL], message=[message], imgHash=[imgHash], postURL=[boardObject['URL']], Title=[boardObject['title']])
