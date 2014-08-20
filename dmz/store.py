"""Implements a db backed storage area for intermediate results"""
import sqlite3


class Store(object):
    """
    Represents an sqlite3 backed storage area that's vaguely key value
    modeled for intermediate storage about metadata / data for metrics
    about multiple wikis that have some underlying country related basis
    """

    _initial_sql_ = [
        'CREATE TABLE IF NOT EXISTS meta (key, value);',
        'CREATE UNIQUE INDEX IF NOT EXISTS meta_key ON meta(key);',
        'CREATE TABLE IF NOT EXISTS wiki_meta (wiki, key, value);',
        'CREATE UNIQUE INDEX IF NOT EXISTS wiki_meta_key ON wiki_meta(wiki, key);',
        'CREATE TABLE IF NOT EXISTS country_info (wiki, country, key, value);',
        'CREATE UNIQUE INDEX IF NOT EXISTS country_info_key ON country_info(wiki, country, key);'
    ]

    def __init__(self, path):
        """Initialize a store at the given path.

        Creates the tables required if they do not exist"""
        self.db = sqlite3.connect(path)
        for sql in Store._initial_sql_:
            self.db.execute(sql)

    def set_meta(self, key, value):
        """Set generic metadata key value, global to the store"""
        self.db.execute("INSERT OR REPLACE INTO meta VALUES (?, ?)", (key, value))
        self.db.commit()

    def get_meta(self, key):
        """Get generic metadata key value, global to the store"""
        try:
            cur = self.db.cursor()
            cur.execute("SELECT value from meta WHERE key = ?", (key, ))
            cur.fetchone()
            return cur[0]
        finally:
            cur.close()

    def set_wiki_meta(self, wiki, key, value):
        """Set wiki specific meta key value"""
        self.db.execute("INSERT OR REPLACE INTO wiki_meta VALUES (?, ?, ?)", (wiki, key, value))
        self.db.commit()

    def get_wiki_meta(self, key):
        """Get wiki specific meta key value"""
        try:
            cur = self.db.cursor()
            cur.execute("SELECT value from wiki_meta WHERE wiki = ? AND key = ?", (wiki, key, ))
            cur.fetchone()
            return cur[0]
        finally:
            cur.close()

    def set_country_info(self, wiki, country, key, value):
        """Set a country and wiki specific key and value"""
        self.db.execute("INSERT OR REPLACE INTO country_info VALUES (?, ?, ?, ?)", (wiki, country, key, value))
        self.db.commit()

    def set_country_info_bulk(self, wiki, key, country_dict):
        """Bulk insert a dictionary of country specific key and value.

        The dictionary should be of form {'country': 'value'}
        """
        insert_data = [(wiki, k, key, v) for (k, v) in country_dict.iteritems()]
        self.db.executemany("INSERT OR REPLACE INTO country_info VALUES (?, ?, ?, ?)", insert_data)
        self.db.commit()

    def get_country_info(self, wiki, country, key):
        """Get a country and wiki specific value for a given key"""
        try:
            cur = self.db.cursor()
            cur.execute("SELECT value from country_info WHERE wiki = ? AND country = ?AND key = ?",
                (wiki, country, key, ))
            cur.fetchone()
            return cur[0]
        finally:
            cur.close()
