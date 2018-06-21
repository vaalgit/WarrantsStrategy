import pytest
from mock import Mock
import sys
import warrants_strategy

class TestMain(object):
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        print('setup_teardown')
        yield

    def test_default_warrants_strategy(self):
        print('test default')

        # assert isinstance(EZLog._handler, logging.StreamHandler)
        # assert EZLog._handler.level == logging.INFO
        # logger = EZLog.get_logger('test_default_logger')
        # assert logger.handlers[0] == EZLog._handler