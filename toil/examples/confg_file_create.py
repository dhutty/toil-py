# -*- coding: utf-8 -*-
"""
toil - A hard working framework on the ground for your cloud
create a config file example
"""
import logging
import traceback
import sys
import toil.util.decorator
import toil.config
import toil.framework
import toil.parm

from toil.batch.base import BaseBatch

logging.basicConfig(format='%(asctime)s %(levelname)s: %(name)s %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class Batch(BaseBatch):

    def create_toil(self):
        # parse args - overrides becasue base method requires -c (config file) in arguments,
        #              since we are generating a config no need to pass one in.
        args = toil.parm.parse.handle_parms()
        logger.debug(args)

        return toil.framework.create(**args)

    @toil.util.decorator.timeit(loops=1)
    def execute(self, framework):
        logger.info('execute')

        try:
            file_name = '/Users/aclove/toil_config.json'
            toil.config.util.generate_config_file(file_name)

        except Exception as ex:
            logger.error(ex)
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logger.error(message)
            traceback.print_exc(file=sys.stdout)


if __name__ == '__main__':
    Batch().run()
