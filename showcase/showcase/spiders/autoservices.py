import scrapy

from showcase.items import Car


class CarMarketSpider(scrapy.Spider):
    name = "cars"
    # Base url used for formatting next page url
    base_url = 'https://someurl.eu'

    def start_requests(self):
        # Start the first request
        url = 'https://someurl.eu/'
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        # Find all ads
        res = response.xpath('//div[contains(@class, "listitem") and contains(@id, "list-item")]')

        # Iterate over found ads and scrape details
        for ad in res:
            price_container = ad.xpath('div[@class="listitem-content-right"]/div/div[@class="listitem-price"]')
            price = price_container.xpath('*/strong/text()').get().strip()
            description = ad.xpath('*/div[@class="listitem-description"]')
            name = description.xpath('a[@class="listitem-link"]/h2/text()').get().strip()
            info = description.xpath('div[@class="listitem-info"]')
            year = info.xpath('span[@class="listitem-info-year"]/text()').get()
            trans = info.xpath('span[@class="listitem-info-trans"]/text()').get()
            fuel = info.xpath('span[@class="listitem-info-fuel"]/text()').get()
            km = info.xpath('span[@class="listitem-info-km"]/text()').get()
            kw = info.xpath('span[@class="listitem-info-kw"]/text()').get()
            date = info.xpath('span[@class="listitem-info-date"]/text()').get().strip()
            images_container = ad.xpath('div[@class="listitem-content-left"]')
            photo = images_container.xpath('a[@class="listitem-photo-link"]')
            img_url = photo.xpath('picture/img/@src').get()
            car = Car(price=price, name=name, year=year, trans=trans,fuel=fuel,
                      km=km, kw=kw, date=date, image_urls=[img_url])
            yield car

        # Find the next page
        next_page = response.xpath('//a[@class="fwd1"]/@href').get()
        # If next page is not null, scrape it
        if next_page is not None:
            yield response.follow(self.base_url + next_page, callback=self.parse)