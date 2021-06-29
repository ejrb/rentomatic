import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration"""


class ProdConfig(Config):
    """Production configuration"""


class DevConfig(Config):
    """Development configuration"""


class TestConfig(Config):
    """Testing configuration"""

    TESTING = True

