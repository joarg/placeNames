import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from cencus.spiders.source_spider import SourceSpider
#from cencus.spiders.person_list_spider import PersonListSpider
#from cencus.spiders.person_info_spider import PersonInfoSpider

def run_spiders():
    print("Starting Crawling Process")  # Add this line
    process = CrawlerProcess(get_project_settings())
    print("CrawlerProcess created")  # Add this line
    process.crawl(SourceSpider)
#    process.join()  # Add this line
#    process.crawl(PersonListSpider)
#    process.crawl(PersonInfoSpider)

    print("First spider crawled")  # Add this line
    process.start()

if __name__ == '__main__':
    run_spiders()
