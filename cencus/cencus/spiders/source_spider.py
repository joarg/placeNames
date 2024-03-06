import scrapy
import json
import random


class SourceSpider(scrapy.Spider):
    name = 'source_spider'

    def __init__(self):
        super().__init__()
        self.accumulated_data = []  # Initialize the list

    def start_requests(self):
        with open('data/sources.json', 'r') as f:
            sources = json.load(f)
            random_sources = random.sample(sources, 2)
        fromSource = 0
        toSource = 10
        
        for source in sources[fromSource:toSource]:
            source_id = source['id']
            year = source['year']
            url = f"https://www.digitalarkivet.no/census/search/{year}/{source_id}?fornavn="
            yield scrapy.Request(url, meta={'source_data': {'id': source['id'], 'year': source['year']}},
                                 callback=self.parse_person_list)

    def parse_person_list(self, response):
        source_data = response.meta['source_data']
        person_links = response.css('a.block-link[href]')
        person_ids = []
        for link in person_links:
            href = link.attrib['href']
            if "/person/" in href:
                person_id = href.split("/person/")[-1]
                person_ids.append(person_id)
        #print(person_ids)

        # Create requests for PersonInfoSpider
        for person_id in person_ids:
            yield scrapy.Request(
                f"https://www.digitalarkivet.no/census/person/{person_id}",
                meta={'source': source_data, 'person_id': person_id}, callback=self.parse_person_info)

    def parse_person_info(self, response):
        try:
            name = response.css(
                'h1:contains("Person: ")::text').getall()[-1].strip()
        except AttributeError:
            name = None

        try:
            personinHouseholdId = response.css(
                '.de-emphasized:nth-child(2)::text').get()
        except AttributeError:
            personinHouseholdId = None

        try:
            Rolle = response.css(
                'div.col-md-6:contains("Rolle:") + div.ssp-semibold::text').get().strip()
        except AttributeError:
            Rolle = None

        try:
            Husholdningsnr = response.css(
                'div.col-md-6:contains("Husholdningsnr:") + div.ssp-semibold::text').get().strip()
        except AttributeError:
            Husholdningsnr = None

        try:
            Personnr = response.css(
                'div.col-md-6:contains("Personnr:") + div.ssp-semibold::text').get().strip()
        except AttributeError:
            Personnr = None

        try:
            Familiestilling = response.css(
                'div.col-md-6:contains("Familiestilling:") + div.ssp-semibold::text').get().strip()
        except AttributeError:
            Familiestilling = None

        try:
            Sivilstand = response.css(
                'div.col-md-6:contains("Sivilstand:") + div.ssp-semibold::text').get().strip()
        except AttributeError:
            Sivilstand = None

        try:
            Yrke = response.css(
                'div.col-md-6:contains("Yrke:") + div.ssp-semibold::text').get().strip()
        except AttributeError:
            Yrke = None

        try:
            Kjønn = response.css(
                'div.col-md-6:contains("Kjønn:") + div.ssp-semibold::text').get().strip()
        except AttributeError:
            Kjønn = None

        try:
            Alder = response.css(
                'div.col-md-6:contains("Alder:") + div.ssp-semibold::text').get().strip()
        except AttributeError:
            Alder = None

        try:
            Fødselsdato = response.css(
                'div.col-md-6:contains("Fødselsdato:") + div.ssp-semibold::text').get().strip()
        except AttributeError:
            Fødselsdato = None

        try:
            Fødested = response.css(
                'div.col-md-6:contains("Fødested:") + div.ssp-semibold::text').get().strip()
        except AttributeError:
            Fødested = None

        try:
            Bostatus = response.css(
                'div.col-md-6:contains("Bostatus:") + div.ssp-semibold::text').get().strip()
        except AttributeError:
            Bostatus = None

        try:
            Sedvanlig_bosted = response.css(
                'div.col-md-6:contains("Sedvanlig bosted:") + div.ssp-semibold::text').get().strip()
        except AttributeError:
            Sedvanlig_bosted = None

        try:
            Antatt_oppholdssted = response.css(
                'div.col-md-6:contains("Antatt oppholdssted:") + div.ssp-semibold::text').get().strip()
        except AttributeError:
            Antatt_oppholdssted = None

        try:
            kildeinformasjon = response.css(
                'p.ssp-semibold::text').get().strip()
        except AttributeError:
            kildeinformasjon = None

        try:
            fylke = response.css(
                'div.col-xs-6:contains("Fylke:") + div.ssp-semibold::text').get().strip()
        except AttributeError:
            fylke = None

        try:
            kommune_1947 = response.css(
                'div.col-xs-6:contains("Kommune (1947):") + div.ssp-semibold::text').get().strip()
        except AttributeError:
            kommune_1947 = None

        try:
            geografisk_omrade = response.css(
                'div.col-xs-6:contains("Geografisk område:") + div.ssp-semibold::text').get().strip()
        except AttributeError:
            geografisk_omrade = None

        try:
            startar = response.css(
                'div.col-xs-6:contains("Startår:") + div.ssp-semibold::text').get().strip()
        except AttributeError:
            startar = None

        try:
            sluttar = response.css(
                'div.col-xs-6:contains("Sluttår:") + div.ssp-semibold::text').get().strip()
        except AttributeError:
            sluttar = None

        try:
            tellingskrets = response.css(
                'h4:contains("Tellingskrets:") + p a::text').get().strip().replace('\t', ' ').replace('  ', ' ')
        except AttributeError:
            tellingskrets = None

        try:
            bosted_by = None
            bosted_land = None
            bosted_by = None
            leilighet_nummer = None
            leilighet_plassering = None
            leilighet_etasje = None
            matr_gnr = None
            lopenr_bnr = None

            if response.css('h4:contains("Bosted land:")'):  # Small area condition
                try:
                    # Extract Matr.nr/Gnr and Løpenr/Bnr
                    matr_gnr = response.css(
                        'div.parent div.row:contains("Matr.nr/Gnr:") div.ssp-semibold::text').get().strip()
                except AttributeError:
                    matr_gnr = None

                try:
                    lopenr_bnr = response.css(
                        'div.parent div.row:contains("Løpenr/Bnr:") div.ssp-semibold::text').get().strip()
                except AttributeError:
                    lopenr_bnr = None

                try:
                    bosted_land = response.css('h4:contains("Bosted land:") + p a::text').get(
                    ).replace('\t', ' ').replace('  ', ' ').replace('\n', '').strip()
                except AttributeError:
                    bosted_land = None

                # Set other properties to None since they are not applicable
                    bosted_by = None
                    leilighet_nummer = None
                    leilighet_plassering = None
                    leilighet_etasje = None

            # City / Larger area
            elif response.css('h4:contains("Bosted by:") + p a::text').get():
                try:
                    bosted_by = response.css(
                        'h4:contains("Bosted by:") + p a::text').get().replace('\t', ' ').replace('  ', ' ')
                except AttributeError:
                    bosted_by = None

                try:
                    leilighet_nummer = response.css(
                        'h4:contains("Leilighet:") + p a::text').get().strip()
                except AttributeError:
                    leilighet_nummer = None

                try:
                    leilighet_plassering = response.css(
                        'div.row:contains("Plassering:") + div.ssp-semibold::text').get()
                except AttributeError:
                    leilighet_plassering = None

                try:
                    leilighet_etasje = response.css(
                        'div.row:contains("Etasje:") + div.ssp-semibold::text').get()
                except AttributeError:
                    leilighet_etasje = None

                # Set Matr.nr./Gnr and Løpenr/Bnr to None
                matr_gnr = None
                lopenr_bnr = None

            else:
                print('No bosted by or land')

        except AttributeError:
            print('No bosted by or land')
        results = {
            'name': name,
            'personinHouseholdId': personinHouseholdId,
            'Rolle': Rolle,
            'Husholdningsnr': Husholdningsnr,
            'Personnr': Personnr,
            'Familiestilling': Familiestilling,
            'Sivilstand': Sivilstand,
            'Yrke': Yrke,
            'Kjønn': Kjønn,
            'Alder': Alder,
            'Fødselsdato': Fødselsdato,
            'Fødested': Fødested,
            'Bostatus': Bostatus,
            'Sedvanlig_bosted': Sedvanlig_bosted,
            'Antatt_oppholdssted': Antatt_oppholdssted,
            'kildeinformasjon': kildeinformasjon,
            'fylke': fylke,
            'kommune_1947': kommune_1947,
            'geografisk_omrade': geografisk_omrade,
            'startar': startar,
            'sluttar': sluttar,
            'tellingskrets': tellingskrets,
            'bosted_by': bosted_by,
            'leilighet_nummer': leilighet_nummer,
            'leilighet_plassering': leilighet_plassering,
            'leilighet_etasje': leilighet_etasje,
            'bosted_land': bosted_land,
            'matr_gnr': matr_gnr,
            'lopenr_bnr': lopenr_bnr,
            'url': response.url,
        }
        self.accumulated_data.append(results)

    def closed(self, reason):
        with open(f'output_{self.fromSource}_{self.toSource}.json', 'w') as f:  # Use 'w' mode for writing
            json.dump(self.accumulated_data, f, ensure_ascii=False)
