import sys
import os
import yaml
from dateutil import parser
from runner import Runner
from processors import editor_countries
from datetime import datetime
import argparse

__dir__ = os.path.dirname(__file__)

if __name__ == '__main__':
    config = yaml.load(open(os.path.join(__dir__, 'config.yaml')))

    arg_parser = argparse.ArgumentParser(description='Run SQL processors against a wiki database')
    arg_parser.add_argument('--wikis', nargs='+', help='DBName of Wikis to run stats for')
    arg_parser.add_argument('--wiki-class', nargs='+', help='Classes of Wikis to run stats for')
    arg_parser.add_argument('--start-date', help='Date to start counting stats from')
    arg_parser.add_argument('--end-date', help='Date till which to count stats for')
    arg_parser.add_argument('processors', nargs='+', help='List of processors to run')

    args = arg_parser.parse_args()

    wikis = []
    if args.wiki_class:
        wikis_data = yaml.load(open('dbnames.json'))
        for wiki_class in args.wiki_class:
            wikis.extend(wikis_data[wiki_class])
    if args.wikis:
        wikis.extend(args.wikis)
    if not wikis:
        print "Must specify at least one of --wikis or --wiki-class"
        sys.exit(-1)

    start_date = parser.parse(args.start_date)
    end_date = parser.parse(args.end_date)
    runner = Runner(config)
    runner.register_processor(editor_countries.edits_per_country)


    print 'Starting runs for %s wikis for data from %s to %s' % (
        len(wikis), start_date.isoformat(), end_date.isoformat()
    )
    for wiki in wikis:
        print 'Running for wiki %s' % wiki
        for processor_name in args.processors:
            runner.run_processor(processor_name, wiki, start_date, end_date)
