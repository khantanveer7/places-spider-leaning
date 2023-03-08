import scrapy

class EdgarsspiderSpider(scrapy.Spider):
    name = 'edgarsspider'
    allowed_domains = ['edgars.co.za/stores']
    start_urls = ['https://www.edgars.co.za/stores']

    def parse (self, response):
        for store in response.css('ol.products.list.items.product-items'):
         name = store.css("a.product-item-link::text").extract()
         description = store.css("div.product-item-description::text").extract()
         link = store.css("a.product-item-link::attr(href)").extract()
         hours = store.css("div.product-open-until::text").extract()
         location = store.css("a.visible-xs.directions::attr(href)").extract()
        yield{
            'name': name,
            'store_url':link,
            'extras': description,
            'opening_hours': hours,
            'addr_full':location,}
            

           

        
          
            
            
           

        
        

        
            
            
            
                
            
            
           
            

            
            
        
            
            