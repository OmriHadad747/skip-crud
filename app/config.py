from os import environ
from dotenv import load_dotenv


load_dotenv()


class BaseConfig:
    SECRET_KEY = environ.get("SECRET_KEY")


class ProdConfig(BaseConfig):
    # General flask's configuration
    ENV = "production"
    FLASK_ENV = "production"
    TESTING = False
    DEBUG = False

    # MongoDB
    MONGO_URI = environ.get("MONGO_URI_PROD")
    CUSTOMER_COLLECTION = environ.get("CUSTOMER_COLLECTION_PROD")
    FREELANCER_COLLECTION = environ.get("FREELANCER_COLLECTION_PROD")
    JOB_COLLECTION = environ.get("JOB_COLLECTION_PROD")


class DevConfig(BaseConfig):
    # General flask's configuration
    ENV = "development"
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = False

    # JWT
    JWT_ACCESS_TOKEN_EXPIRES = False

    # MongoDB
    MONGO_URI = environ.get("MONGO_URI_DEV")
    CUSTOMER_COLLECTION = environ.get("CUSTOMER_COLLECTION_DEV")
    FREELANCER_COLLECTION = environ.get("FREELANCER_COLLECTION_DEV")
    JOB_COLLECTION = environ.get("JOB_COLLECTION_DEV")

    # Redis
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_DB = 0

    # freelancer-finder service
    FREELANCER_FINDER_HOST = "localhost:4999"


class TestConfig(BaseConfig):
    # General flask's configuration
    ENV = "testing"
    FLASK_ENV = "testing"
    DEBUG = False
    TESTING = True

    # JWT
    JWT_ACCESS_TOKEN_EXPIRES = False

    # MongoDB
    MONGO_URI = environ.get("MONGO_URI_TEST")
    CUSTOMER_COLLECTION = environ.get("CUSTOMER_COLLECTION_TEST")
    FREELANCER_COLLECTION = environ.get("FREELANCERS_COLLECTION_TEST")
    JOB_COLLECTION = environ.get("JOB_COLLECTION_TEST")
