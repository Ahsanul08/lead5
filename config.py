from configparser import ConfigParser
from datetime import date

parser = ConfigParser()
parser.read('config.ini')

start_url = 'http://www.lead5media.com/'

username = parser.get('credentials', 'username')
password = parser.get('credentials', 'password')

wait_timeout = parser.getint('wait', 'wait_timeout')

begin_date = date(parser.getint('begin_date', 'year'), parser.getint('begin_date', 'month'),
                  parser.getint('begin_date', 'day'))
end_date = date(parser.getint('end_date', 'year'), parser.getint('end_date', 'month'), parser.getint('end_date', 'day'))
