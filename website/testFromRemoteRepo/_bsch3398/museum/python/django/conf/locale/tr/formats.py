# -*- encoding: utf-8 -*-
# This file is distributed under the same license as the Django package.
#

DATE_FORMAT = 'd F Y'
TIME_FORMAT = 'H:i:s'
DATETIME_FORMAT = 'd F Y H:i:s'
YEAR_MONTH_FORMAT = 'F Y'
MONTH_DAY_FORMAT = 'd F'
SHORT_DATE_FORMAT = 'd M Y'
SHORT_DATETIME_FORMAT = 'd M Y H:i:s'
FIRST_DAY_OF_WEEK = 1 # Pazartesi
DATE_INPUT_FORMATS = (
    '%d/%m/%Y', '%d/%m/%y', # '25/10/2006', '25/10/06'
    '%Y-%m-%d', '%y-%m-%d',     # '2006-10-25', '06-10-25'
    # '%d %B %Y', '%d %b. %Y',  # '25 Ekim 2006', '25 Eki. 2006'
)
TIME_INPUT_FORMATS = (
    '%H:%M:%S', # '14:30:59'
    '%H:%M',    # '14:30'
)
DATETIME_INPUT_FORMATS = (
    '%d/%m/%Y %H:%M:%S', # '25/10/2006 14:30:59'
    '%d/%m/%Y %H:%M', # '25/10/2006 14:30'
    '%d/%m/%Y', # '25/10/2006'
    '%Y-%m-%d %H:%M:%S', # '2006-10-25 14:30:59'
    '%Y-%m-%d %H:%M', # '2006-10-25 14:30'
    '%Y-%m-%d',             # '2006-10-25'
)
DECIMAL_SEPARATOR = ','
THOUSAND_SEPARATOR = '.'
NUMBER_GROUPING = 3
