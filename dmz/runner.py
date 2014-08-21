"""Helper class to register and run processor functions

A processor function runs a query against the db, performs some augmentation on the
data, and stores the results in a store.

They have the following signature:
    def processor_function(runner, wiki, start_time, end_time, **kwargs)

    runner is the Runner instance they can use to access the store and db.
    wiki is the dbname of the wiki to run queries against
    start_time is a datetime instance specifying the date from which to include data
    end_time is a datetime instance specifying the date till which to include data
    **kwargs is any aditional parameters the runner might require

DB Host and other details are gleamed from a config dict passed in"""
from store import Store
import MySQLdb as mysql


class Runner(object):
    """
    Runs a set of queries / processor functions that write their results to the same Store
    """
    def __init__(self, config):
        self.store = Store(config['STORE_PATH'])
        self.config = config
        self.processors = {}


    @property
    def db(self):
        """A mysql database connection to be used for running queries"""
        if not hasattr(self, '_db'):
            self._db = mysql.connect(
                host=self.config['DB_HOST'],
                read_default_file=self.config.get('DB_DEFAULTS_FILE', '~/.my.cnf')
            )
        return self._db


    def register_processor(self, processor):
        """Register a processor function that can be called by name later"""
        self.processors[processor.__name__] = processor

    def run_processor(self, processor_name, wiki, start_time, end_time, kwargs={}):
        """Run a processor function by name against a particular wiki"""
        processor = self.processors[processor_name]
        processor(self, wiki, start_time, end_time, **kwargs)
