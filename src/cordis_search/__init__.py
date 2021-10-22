from .wrapper import search, summary
from .constants import SEPARATOR

import logging
import sys

logging.basicConfig(stream=sys.stdout, format='%(asctime)s: %(name)s / %(levelname)s - %(message)s', level=logging.INFO)