import scrapy


class PersonIDSpider(scrapy.Spider):
    name = 'personId_spider'
    print("inside spiderclass")

    def start_requests(self, year, source_id):
        print('inside start_requests of personId_spider')
        try:
            url = f"https://www.digitalarkivet.no/census/search/{year}/{source_id}?fornavn="
            print('url is set to...', url)
            request = scrapy.Request(url=url, callback=self.parse_person_ids)
            yield request

        except Exception as e:
            print("Error in start_requests: ", e)

    def parse_person_ids(self, response):
        print('parsing person_ids')
        # print("DEBUG: Inside parse_person_ids, response.body:", response.body)  # Add here
        # print('body', response.body)
        person_links = response.css('a.block-link[href]')
        person_ids = []
        for link in person_links:
            href = link.attrib['href']
            if "/person/" in href:
                person_id = href.split("/person/")[-1]
                person_ids.append(person_id)
        yield {'person_ids': person_ids}
