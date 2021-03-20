import scrapy

from showcase.items import Car


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://skoda-superb.autobazar.eu/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        res = response.xpath('//div[contains(@class, "listitem") and contains(@id, "list-item")]')
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

        # page = response.url.split("/")[-2]
        # filename = f'quotes-{page}.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log(f'Saved file {filename}')