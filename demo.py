

from shipment.logger import logging
from shipment.exception import shippingException
import sys

try:
    a=1/0
except Exception as e:
    logging.info(e)
    raise shippingException(e,sys) from e
