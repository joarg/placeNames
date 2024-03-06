import scrapy
import json
import re

class SourcesSpider(scrapy.Spider):
    name = 'sources_spider'
    start_urls = [
        'https://www.digitalarkivet.no/search/sources?s=&from=&to=&format=tab_ftr&archive_key=&sc%5B0%5D=ft']


    def parse(self, response):
        # Process the current page
        for source_unit in response.css('div.unit'):
            source_id = source_unit.css(
                'div.name a::attr(href)').get().split('/')[-1]
            name = source_unit.css('div.name a::text').get().strip()

            # Extract archive using xpath to get the desired text node
            archive = source_unit.xpath(
                './/div[@class="archive"]/text()[normalize-space()]').get()

            year = re.search(r'\d{4}', name)  # Search for a 4-digit year
            if year:
                year = year.group(0)  # Extract the matched year
            else:
                year = None  # Handle cases where no year is found
            yield {
                'id': source_id,
                'name': name,
                'archive': archive,
                'year': year
            }
        # Follow pagination
        next_page_link = response.css('a[title="Neste"]::attr(href)').get()
        if next_page_link:
            yield response.follow(next_page_link, callback=self.parse)
