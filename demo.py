

from shipment.logger import logging
from shipment.exception import shippingException
import sys
from shipment.utils.main_utils import MainUtils


obj=MainUtils()

data=obj.read_yaml_file("config/model.yaml")
print(data)
