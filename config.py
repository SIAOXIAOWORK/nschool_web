class Config(object):
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True

class TestingConfig(Config):
    ENV = "testing"
    TESTING = True