import logging

logging.basicConfig(
    filename='split_phones.log', # /var/log/split_phones.log
    level=logging.DEBUG, 
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%d-%b-%y %H:%M:%S'
    )

logger = logging.getLogger()

# отключаем стандартный логгер flask
logging.getLogger('werkzeug').disabled = True
