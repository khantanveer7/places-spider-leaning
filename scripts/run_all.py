from scrapy.crawler import CrawlerProcess
from scrapy import spiderloader
from scrapy.utils import project

settings = project.get_project_settings()
spider_loader = spiderloader.SpiderLoader.from_settings(settings)
spiders = spider_loader.list()
classes = [spider_loader.load(name) for name in spiders]

process = CrawlerProcess(settings=settings)

# for spider_class in classes:
#     spider_class.custom_settings = {
#         'FEEDS': {
#             f'all_poi.csv': {
#                 'format': 'csv', 
#                 'encoding': 'utf8'
#             },
#         },
#     }
#     process.crawl(spider_class)

for spider_class in classes:
    spider_class.custom_settings = {
        'FEEDS': {
            f'{spider_class.name}.csv': {
                'format': 'csv', 
                'encoding': 'utf8'
            },
             f'all_poi.csv': {
                'format': 'csv', 
                'encoding': 'utf8'
            },
        },
    }
    process.crawl(spider_class)

process.start()