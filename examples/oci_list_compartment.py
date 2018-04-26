# -*- coding: utf-8 -*-
"""
toil - A hard working framework on the ground for your cloud
oci compartment list example
"""
import logging
import traceback
import sys
import util.decorator
from batch.base import BaseBatch


logging.basicConfig(format='%(asctime)s %(levelname)s: %(name)s %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class Batch(BaseBatch):

    @util.decorator.timeit(loops=1)
    def execute(self, framework):
        logger.info('execute')

        try:

            env = "oci_profile_1"

            logger.info("processing env:{env}".format(env=env))
            session = framework.oci.session(env)
            identity_client = session.client('identity')
            tenancy = session.config()['tenancy']
            compartments = session.paginate(identity_client.list_compartments, tenancy)

            for compartment in compartments:
                logger.info(compartment)

        except Exception as ex:
            logger.error(ex)
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logger.error(message)
            traceback.print_exc(file=sys.stdout)


if __name__ == '__main__':
    Batch().run()
