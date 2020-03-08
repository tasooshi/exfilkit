import logging
import sys


__version__ = '1.0'


logger = logging.getLogger('lollipopz')
formatter = {
    logging.DEBUG: logging.Formatter('%(name)s %(levelname)s [%(asctime)s] %(message)s'),
    logging.INFO: logging.Formatter('%(message)s')
}
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)
