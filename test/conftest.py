import pytest
import sys
import mock

sys.modules['DataFetcher.crawl'] = mock.Mock()
