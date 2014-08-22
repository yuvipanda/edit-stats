"""Generate JSON files with dbnames per project

Just generates for wikipedias for now"""
from urllib2 import urlopen
import unicodecsv as csv
import json


def get_dbnames(wiki_class):
    """Return dbnames for all wikis in a particular wiki_class, such as 'wikipedias'"""
    URL = "https://wikistats.wmflabs.org/api.php?action=dump&table=%s&format=csv&s=good" % wiki_class

    data = csv.reader(urlopen(URL))

    dbnames = []
    is_first = True
    for row in data:
        if is_first:
            is_first = False
            continue  # skip headers!
        # dbnames is just langcode with - replaced by _ and a 'wiki' suffix
        dbnames.append(u'%swiki' % (row[2].replace('-', '_'), ))

    return dbnames

data = {
    'wikipedias': get_dbnames("wikipedias")
}
json.dump(data, open('dbnames.json', 'w'))

