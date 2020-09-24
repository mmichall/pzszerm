# -*- coding: utf-8 -*-
import scrapy

from crawlers.items import Tireur
import gender_guesser.detector as gender

gender_detector = gender.Detector()

map = {'Klub': 'Club', 'Data urodzenia': 'DateNaissance', 'Licencja PZS': 'Licence'}


class PzszermSpider(scrapy.Spider):
    name = 'pzszerm'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def start_requests(self):
        urls = [
            'http://www.pzszerm.pl/zawodnicy/zawodnik/{}'.format(i + 1) for i in range(50_000)
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        tireur = Tireur()
        name_surename = response.xpath('//div[@class="zawodnik"]//h1/text()').get()
        if name_surename:
            name_surename = name_surename.replace('Zawodnik: ', '').split(' ')
            tireur['ID'] = response.url.split('/')[-1]
            tireur['Prenom'] = name_surename[0]
            tireur['Nom'] = name_surename[1]
            fields = response.xpath('//div[@class="zawodnik"]//tr')
            for field in fields:
                value = field.xpath('td/text()').extract()
                value[0] = value[0].replace(':', '')
                if value[0] in map:
                    tireur[map[value[0]]] = value[1]
            tireur['Sexe'] = gender_detector.get_gender(name_surename[0], u'poland')
            tireur['Nation'] = 'POL'
            tireur['Statut'] = 'N'
            return tireur

    def remove_tags(self, value: str, tags):
        for tag in tags:
            value = value.replace(tag, '')
        return value
