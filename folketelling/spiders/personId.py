import scrapy
class PersonSpider(scrapy.Spider):
    name = 'personId_spider'
    print("inside spiderclass")
    def start_requests(self):
        print("inside start_requests")
        year = getattr(self, 'year', 2022)  # Replace with the desired year
        source_id = getattr(self, 'source_id', 12345)  # Replace with the desired source ID
        url = f"https://www.digitalarkivet.no/census/search/{year}/{source_id}?fornavn="
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print("inside parse")
        person_links = response.css('a.block-link[href]') 
        person_ids = []
        for link in person_links:
            href = link.attrib['href']
            if "/person/" in href:
                person_id = href.split("/person/")[-1]
                person_ids.append(person_id)
        yield {'person_ids': person_ids}