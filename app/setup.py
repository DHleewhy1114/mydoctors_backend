from ast import literal_eval
import models
import logging
import sys
"""
# Load logging configuration
log = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
"""

if __name__ == '__main__':
    #log.info('Create database {}'.format(base.db_name))
    models.Base.metadata.create_all(models.engine)
