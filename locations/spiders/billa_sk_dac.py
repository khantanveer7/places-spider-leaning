import scrapy
from locations.items import GeojsonPointItem


class GomexSpider(scrapy.Spider):
    name = 'billa_sk_dac'
    allowed_domains = ['billa.sk']
    
    def start_requests(self):
        url = 'https://www.billa.sk/api/stores/all'
        
        headers = {
            "lat": "48.1458923",
            "lon": "17.1071373",
        }

        yield scrapy.Request(
            url=url, 
            method='GET', 
            headers=headers,
            callback=self.parse,
        )

    def parse(self, response):
        data = response.json()
        
        for row in data["groupedStores"]["84"]:
            item = GeojsonPointItem()

            country = "Slovakia"
            city = row.get("city")
            street = row.get("street")
            province = row.get("province").get("provinceName")

            item['ref'] = row.get("storeId")
            item['brand'] = 'BILLA'
            item["name"] = row.get("displayName")
            item['addr_full'] = f"{country},{province},{city},{street}"
            item['city'] = city
            item['state'] = province
            item["street"] = street
            item['country'] = country
            item['phone'] = f'{row.get("telephoneAreaCode")}, {row.get("telephoneNumber")}'
            item["postcode"] = row.get("zip")
            item['website'] = "https://www.billa.sk/"
            item['email'] = "info@billa.sk"
            item["opening_hours"] = row.get("openingTimesHTMLSplit")
            item['lat'] = row.get("yCoordinates")
            item['lon'] = row.get("xCoordinates")

            yield item