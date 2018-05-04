# -*- coding: utf-8 -*-
"""
toil - A hard working framework on the ground for your cloud
encryption example
"""
import logging
import traceback
import sys
import toil.util.decorator
from toil.batch.base import BaseBatch

logging.basicConfig(format='%(asctime)s %(levelname)s: %(name)s %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class Batch(BaseBatch):

    @toil.util.decorator.timeit(loops=1)
    def execute(self, framework):
        logger.info('execute')

        try:

            encryptor = framework.encryptor
            key = encryptor.generate_key("/Users/aclove/testkey.dat")

            confidential_data = "this is an encryption data test"
            logger.info("confidential_data:{confidential_data}".format(confidential_data=confidential_data))

            encrypted_data = encryptor.encrypt(confidential_data, encryption_key=key)
            logger.info("encrypted_data:{encrypted_data}".format(encrypted_data=encrypted_data))

            decrypted_data = encryptor.decrypt(encrypted_data, encryption_key=key)
            logger.info("decrypted_data:{decrypted_data}".format(decrypted_data=decrypted_data))

        except Exception as ex:
            logger.error(ex)
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logger.error(message)
            traceback.print_exc(file=sys.stdout)


if __name__ == '__main__':
    Batch().run()
