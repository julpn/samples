from multiprocessing import Process, Queue
import requests
import urllib2
import base64
import json
import sys
import ssl
import Proc
import time
import math
import logging
import datetime
import _mysql_exceptions
from Queue import Empty

CHUNK_SIZE = 2 ** 17
NEW_LINE = '\r\n'
MAX_RETRIES = 5

URL = 'https://stream.gnip.com:443/accounts/PorterNovelli/publishers/twitter/streams/track/prod.json'
UN = myusername
PWD = mypassword
HEADERS = {'Accept': 'application/json',
           'Connection': 'Keep-Alive',
           'Accept-Encoding': 'gzip',
           'Authorization': 'Basic %s' % base64.encodestring('%s:%s' % (UN, PWD))}

LOG_FILENAME = 'error_log.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

def reader(queue,i):
    ## Read from the queue
    while True:
        try:
            msg = queue.get()      
            string_me = json.loads(msg)
            post = Proc.get_fields(string_me)
            post.insert_time()
        except:
            e = sys.exc_info()[0]
            logging.error(datetime.datetime.now(),'other error, ', exc_info=full_exc_info())
            pass
        print str(msg)

def writer():
    for i in range(MAX_RETRIES):
        response = requests.get(URL, headers=HEADERS, stream=True,timeout=20)
        for chunk in response.iter_lines(chunk_size=15):
            if chunk:
                queue.put(chunk)

def action(jrec):
    post = Proc.get_fields(jrec)
    post.insert_time()
    print str(jrec)

class FauxTb(object):
    def __init__(self, tb_frame, tb_lineno, tb_next):
        self.tb_frame = tb_frame
        self.tb_lineno = tb_lineno
        self.tb_next = tb_next

def current_stack(skip=0):
    try: 1/0
    except ZeroDivisionError:
        f = sys.exc_info()[2].tb_frame
    for i in xrange(skip + 2):
        f = f.f_back
    lst = []
    while f is not None:
        lst.append((f, f.f_lineno))
        f = f.f_back
    return lst

def extend_traceback(tb, stack):
    """Extend traceback with stack info."""
    head = tb
    for tb_frame, tb_lineno in stack:
        head = FauxTb(tb_frame, tb_lineno, head)
    return head

def full_exc_info():
    """Like sys.exc_info, but includes the full traceback."""
    t, v, tb = sys.exc_info()
    full_tb = extend_traceback(tb, current_stack(1))
    return t, v, full_tb

if __name__ == '__main__':
    x = 2
    while True and x <66000:
        try:
            queue = Queue()   # reader() reads from queue
                              # writer() writes to queue
            jobs = []
            for i in range(2):
                reader_p = Process(target=reader, args=(queue,i))
                reader_p.daemon = True
                jobs.append(reader_p)
                reader_p.start()        # Launch reader() as a separate python process

            _start = time.time()
            writer()    # Send a lot of stuff to reader()
            reader_p.join()         # Wait for the reader to finish
        except ssl.SSLError, e:
            logging.error(datetime.datetime.now(), exc_info=full_exc_info())
            r = e
            logging.error(datetime.datetime.now(), 'SSLError, ', exc_info=full_exc_info())
            pass
        except urllib2.URLError, error:
            x = math.pow(x,2)
            print "Sleeping for " + str(x)
            time.sleep(x)
            print "trying to reconnect"
            logging.error(datetime.datetime.now(), 'URLERROR, ', exc_info=full_exc_info())
            pass
        except _mysql_exceptions.OperationalError, e:
            f = sys.exc_info()[0]
            logging.error(datetime.datetime.now(),'other error, ' + e + f, exc_info=full_exc_info())
            time.sleep(10)
            pass
        except Empty:
            pass
        except:
            e = sys.exc_info()[0]
            logging.error(datetime.datetime.now(),'other error, ', exc_info=full_exc_info())
            time.sleep(10)
            pass
        else:
            e = sys.exc_info()[0]
            logging.error(datetime.datetime.now(),'other error, ', exc_info=full_exc_info())
            time.sleep(10)
            pass
