# -*- coding: utf-8 -*-

import scrapy
import re
from datetime import date, timedelta


def id_serialzier(value: str):
    return value


def localization_serializer(value: str):
    return [_loc.strip() for _loc in value.split(',')]


def date_serializer(value: str):
    _date = date.today()
    _value = value.lower()
    if 'około' in value:
        val_arr = _value.split()
        _value = ' '.join([word for word in val_arr[1:len(val_arr)]])
    if 'dzień' in _value or 'wczoraj' in _value:
        _date = _date - timedelta(days=1)
    elif 'godzinę' in _value or 'godzin' in _value or 'godziny' in _value:
        _date = _date
    elif 'dzisiaj'in _value:
        _date = _date
    elif 'dni' in _value:
        _date = _date - timedelta(days=int(_value.split()[0]))
    elif 'miesiące' in _value or 'miesięcy' in _value:
        _date = _date - timedelta(days=30 * int(_value.split()[0]))
    elif 'miesiąc' in _value:
        _date = _date - timedelta(days=30)
    elif 'rok' in _value:
        if _value.startswith('ponad'):
            _date = _date - timedelta(days=365 * 1.5)
        else:
            _date = _date - timedelta(days=365)
    elif 'lata' in _value:
        val_arr = _value.split()
        if _value.startswith('ponad'):
            _date = _date - timedelta(days=365 * int(val_arr[1]))
        else:
            _date = _date - timedelta(days=365 * int(val_arr[0]))
    else:
        return value

    return _date.strftime('%y%m%d')


def only_numeric(value: str):
    _value = re.sub("[^0-9,.]", "", value)
    return _value.replace(",", ".")


def only_numeric_int(value: str):
    if value:
        numeric = only_numeric(value)
        if numeric.isnumeric():
            return int(numeric)
        else:
            return value
    else:
        return value


def only_numeric_float(value: str):
    if value:
        numeric = only_numeric(value)
        if numeric.replace('.','').isnumeric():
            return float(numeric)
        else:
            return value
    else:
        return value


def sex_normalizer(value: str):
    if value == 'male':
        return 'M'
    elif value == 'female':
        return 'F'
    else:
        return 'M'


def date_serializer(_date: str):
    __date: date = date.fromisoformat(_date)
    return __date.strftime('%d.%m.%Y')

def licence_serializer(licence: str):
    if licence:
        _licence = licence.split(' ')[0]
    else:
        _licence = ''
    return _licence

class Tireur(scrapy.Item):

    ID = scrapy.Field(serializer=id_serialzier)
    url = scrapy.Field()
    Prenom = scrapy.Field()
    Nom = scrapy.Field()
    Sexe = scrapy.Field(serializer=sex_normalizer)
    Club = scrapy.Field()
    Nation = scrapy.Field()
    Statut = scrapy.Field()
    DateNaissance = scrapy.Field(serializer=date_serializer)
    Classement = scrapy.Field()
    Licence = scrapy.Field(serializer=licence_serializer)

