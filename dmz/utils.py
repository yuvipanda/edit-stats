def as_mw_date(date):
    """Formats a datetime object into mediawiki style datetime"""
    return date.strftime('%Y%m%d%H%M%S')