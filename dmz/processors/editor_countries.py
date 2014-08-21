#!/usr/bin/env python
"""Count number of edits per country"""
from geolocate import GeoLocator
import utils
from datetime import datetime

def edits_per_country(runner, wiki, start_time, end_time):
    """Generate number of edits per country from given db, starting at start_time until end_time"""
    grouped_ip_sql = """
    SELECT cuc_ip, COUNT(*) as edits
    FROM cu_changes
    WHERE cuc_namespace = 0
        AND cuc_timestamp > %s
        AND cuc_timestamp < %s
        AND cuc_user NOT IN (SELECT ug_user FROM user_groups WHERE ug_group = 'bot')
    GROUP BY cuc_ip
    """
    if not hasattr(runner, 'locator'):
        runner.locator = GeoLocator()

    data = {}

    cur = runner.db.cursor()
    try:
        i = 0
        print "Starting to execute"
        cur.execute('USE %s' % (wiki, ))
        cur.execute(grouped_ip_sql, (utils.as_mw_date(start_time), utils.as_mw_date(end_time)))
        rows = cur.fetchmany(1000)
        while rows:
            for row in rows:
                i += 1
                if row[0].startswith('10.') or row[0].startswith('192.'):
                    country = 'labs'
                else:
                    country = runner.locator.find_country(row[0])
                if country in data:
                    data[country] += row[1]
                else:
                    data[country] = row[1]
            rows = cur.fetchmany(1000)
            print 'done %s' % i

        runner.store.set_country_info_bulk(wiki, 'edits', data)
    finally:
        cur.close()

