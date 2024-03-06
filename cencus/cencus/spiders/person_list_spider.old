import scrapy


class PersonListSpider(scrapy.Spider):
    name = 'person_list_spider'

    def parse(self, response):
        source_data = response.meta['source_data'] 

        person_links = response.css('a.block-link[href]')
        person_ids = []
        for link in person_links:
            href = link.attrib['href']
            if "/person/" in href:
                person_id = href.split("/person/")[-1]
                person_ids.append(person_id)

        # Create requests for PersonInfoSpider
        for person_id in person_ids:
             yield scrapy.Request(
                  f"https://www.digitalarkivet.no/census/person/pf010{person_id}", 
                  meta={'source': source, 'person_id': person_id}
             )