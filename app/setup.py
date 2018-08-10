from ast import literal_eval
#from models import User, Category, Board, Comment
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
"""
    log.info('Insert Planet data in database')
    with open('database/data/planet.json', 'r') as file:
        data = literal_eval(file.read())
        for record in data:
            planet = ModelPlanet(**record)
            base.db_session.add(planet)
        base.db_session.commit()

    log.info('Insert People data in database')
    with open('database/data/people.json', 'r') as file:
        data = literal_eval(file.read())
        for record in data:
            planet = ModelPeople(**record)
            base.db_session.add(planet)
        base.db_session.commit()
"""