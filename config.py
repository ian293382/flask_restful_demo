class Config(object):
  TESTING = False
  DEBUG = False

class DevelopmentConfig(Config):
  ENV= "development"
  DEBUG = True

class TestingConfig(Config):
  ENV = "test"
  TESTING= True