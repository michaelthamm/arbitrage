from bottle import route, run, get, static_file, url, view
from collections import defaultdict, namedtuple
from random import random, uniform, randrange
from math import sqrt
import datetime, time
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Timer:    
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start

def initialize_positions():
    #Borrowed browian formula from
    #http://code.activestate.com/recipes/576760-brownian-motion-of-stock/
    dt =0.0002
    sigma = 0.1
    mu = .02
    SECS_PER_DAY = 25200 #covers 9:30 to 4:30
    Position = namedtuple('position', 'date last volume')
    SYMBOLS = {'IBM':Position(date=None,last=149,volume=0),'T':Position(date=None,last=39,volume=0), 
                'AAPL':Position(date=None,last=108,volume=0), 'C':Position(date=None,last=40,volume=0), 'BAC':Position(date=None,last=13,volume=0)} 
    #change to get last from google finance
    positions = defaultdict(list)

    with Timer() as took:
        for ticker, position in SYMBOLS.iteritems():
            price = position.last
            for seconds in xrange(SECS_PER_DAY):
                x = Position(date=None, last=price, volume=randrange(1000,4000))
                positions[ticker].append(x)
                price = round(price + price*(mu-0.5*pow(sigma,2))*dt+sigma*price*sqrt(dt)*uniform(0,1)*(-1 if random() < .5 else 1),2)
                if price < 0:
                    price = 0
    logger.info('Initializing took %.03f sec.' % took.interval)
    return positions
    
@get('/last/<symbol>')
def last(symbol):
    #calulate how many seconds since start and return that item from the list of prices
    time_stamp = time.mktime(datetime.datetime.now().timetuple())
    cell_to_return = int(start_datetime - time_stamp)
    symbol = symbol.upper()
    if symbol.upper() in positions:
        last = positions[symbol][cell_to_return].last
        volume = positions[symbol][cell_to_return].volume
    return json.dumps({'time_stamp':time_stamp, 'symbol':symbol, 'last':last, 'volume':volume})

@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')
    
@route('/chart/<symbol>')
@view('index')
def chart(symbol):
    symbol = symbol.upper()
    if symbol.upper() in positions:
        data_dict = { 'url': url, 'symbol':symbol }
        return data_dict
    
start_datetime = time.mktime(datetime.datetime.now().timetuple())
positions = initialize_positions()
#positions['IBM'][0].last
run(host='localhost', port=8080, debug=True)
