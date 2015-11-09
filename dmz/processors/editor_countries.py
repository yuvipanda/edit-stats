#!/usr/bin/env python
"""Count number of edits per country"""
from geolocate import GeoLocator
import utils
from datetime import datetime

def edits_per_country(runner, wiki, start_time, end_time):
    """Generate number of edits per country from given db, starting at start_time until end_time"""
    grouped_ip_sql = """
    SELECT cuc_ip, COUNT(*) as edits,
        CASE WHEN ts_tags LIKE '%%mobile%%' THEN 'mobile' ELSE 'desktop' END AS source
    FROM cu_changes LEFT JOIN tag_summary ON cuc_this_oldid = ts_rev_id
    WHERE cuc_namespace = 0
        AND cuc_timestamp > %s
        AND cuc_timestamp < %s
        AND cuc_user NOT IN (SELECT ug_user FROM user_groups WHERE ug_group = 'bot')
    GROUP BY cuc_ip, source
    """
    if not hasattr(runner, 'locator'):
        runner.locator = GeoLocator()

    desktop_edits = {}
    mobile_edits = {}
    all_edits = {}

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
                if row[2] == 'desktop':
                    if country in desktop_edits:
                        desktop_edits[country] += row[1]
                    else:
                        desktop_edits[country] = row[1]
                else:
                    if country in mobile_edits:
                        mobile_edits[country] += row[1]
                    else:
                        mobile_edits[country] = row[1]
                if country in all_edits:
                    all_edits[country] += row[1]
                else:
                    all_edits[country] = row[1]

            rows = cur.fetchmany(1000)
            print 'done %s' % i

        runner.store.set_country_info_bulk(wiki, 'desktop_edits', desktop_edits)
        runner.store.set_country_info_bulk(wiki, 'mobile_edits', mobile_edits)
        runner.store.set_country_info_bulk(wiki, 'all_edits', all_edits)

        # Write totals!
        runner.store.set_wiki_meta(wiki, 'desktop_edits', sum(desktop_edits.values()))
        runner.store.set_wiki_meta(wiki, 'mobile_edits', sum(mobile_edits.values()))
        runner.store.set_wiki_meta(wiki, 'all_edits', sum(all_edits.values()))
    finally:
        cur.close()

