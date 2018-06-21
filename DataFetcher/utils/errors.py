
SUCCESS = 0

class GENERAL:
    GENERAL_ERROR = 10000
    INPUT_VALIDATION_ERROR = 10001
    # All error codes in this category must start from 200
    INVALID_NUMBER_FORMAT_ERROR = 200
    RPC_ERROR = 201

class CrawlRuntimeError(RuntimeError):
    pass