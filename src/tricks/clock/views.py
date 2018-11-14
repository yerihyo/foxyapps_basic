from datetime import datetime

import pytz
from flask import make_response

import settings
from utils.utils import dt2timezone
import os
from collections import defaultdict
from datetime import datetime
from urllib.request import urlretrieve
from urllib.parse import urljoin
from zipfile import ZipFile



def str_LOC2timezone(str_LOC):
    try: return pytz.timezone(str_LOC)
    except pytz.exceptions.UnknownTimeZoneError: pass

    h_city2tz_name = create_str_CITY2tz_name()
    h_set = h_city2tz_name[str_LOC]
    if len(h_set)>1: raise Exception()
    if not h_set: raise Exception()

    tz_name = next(iter(h_set))
    return pytz.timezone(tz_name)



def lookup(uuid_COMMAND, str_LOC=None,):
    now_UTC = datetime.now(pytz.utc)

    if str_LOC is None: str_LOC = "America/Los_Angeles"
    tz = str_LOC2timezone(str_LOC)
    now_TZ = dt2timezone(now_UTC, tz)


    str_RESULT = "[{0}] {1}".format(str_LOC, now_TZ.strftime("%Y.%m.%d %I:%M:%S %p"))
    #print(str_LOC, str_RESULT)
    return make_response(str_RESULT)

    # for tzname in h[city]:
    #     now = datetime.now(pytz.timezone(tzname))
    #     print("")
    #     print("%s is in %s timezone" % (city, tzname))
    #     print("Current time in %s is %s" % (city, now.strftime(fmt)))


def create_str_CITY2tz_name():
    basename = 'cities15000' # all cities with a population > 15000 or capitals
    filename = basename+".zip"
    filepath = os.path.join(settings.TMP_DIR,filename)

    # get file
    if not os.path.exists(filepath):
        geonames_url = 'http://download.geonames.org/export/dump/'+filename
        urlretrieve(urljoin(geonames_url, filename), filepath)

    # parse it
    h = defaultdict(set)
    with ZipFile(filepath) as zf, zf.open(basename + '.txt') as file:
        for line in file:
            fields = line.split(b'\t')
            if fields: # geoname table http://download.geonames.org/export/dump/
                name, asciiname, alternatenames = fields[1:4]
                timezone = fields[-2].decode('utf-8').strip()
                if timezone:
                    for city in [name, asciiname] + alternatenames.split(b','):
                        city = city.decode('utf-8').strip()
                        if city:
                            h[city].add(timezone)
    return h

    # print("Number of available city names (with aliases): %d" % len(city2tz))
    #
    # #
    # n = sum((len(timezones) > 1) for city, timezones in city2tz.iteritems())
    # print("")
    # print("Find number of ambigious city names\n "
    #       "(that have more than one associated timezone): %d" % n)
    #
    # #
    # fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    # city = "Zurich"
