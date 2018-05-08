# -*- coding: utf-8 -*-
"""
toil - A hard working framework on the ground for your cloud
oci vertical scale / change shape example
"""
import logging
import sys
import traceback

import toil.util.decorator
from toil.batch.base import BaseBatch

logging.basicConfig(format='%(asctime)s %(levelname)s: %(name)s %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class Batch(BaseBatch):

    @toil.util.decorator.timeit(loops=1)
    def execute(self, framework):
        logger.info('execute')

        try:
            env = "oci_profile_1"
            logger.info("processing env:{env}".format(env=env))
            session = framework.oci.session(env)
            compute_client = session.client('compute1')
            virtual_network_client = session.client("virtualnetwork")

            session.scale_vertical(compute_client, virtual_network_client,
                                   "ocid1.instance.oc1.iad.abuwcljrv6tl22sbsluibyunos4d5v4yeigtprzeiq3slydlrfxhnw7awn7q",
                                   "VM.Standard1.1")

        except Exception as ex:
            logger.error(ex)
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logger.error(message)
            traceback.print_exc(file=sys.stdout)


if __name__ == '__main__':
    Batch().run()
