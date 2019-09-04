import os
from dotenv import load_dotenv, find_dotenv


class Config:
    """
    This is the base class for config. add configs here to share between Testing and Production environment.
    """

    def __init__(self):
        load_dotenv(find_dotenv(usecwd=True))


class ProductionConfig(Config):
    def __init__(self):
        super(ProductionConfig, self).__init__()

        self.TYPEFORM_API_KEY = os.getenv("TYPEFORM_API_KEY")
        self.TYPEFORM_UID = os.getenv("TYPEFORM_UID")
        self.TYPEFORM_FIRST_NAME_ID = os.getenv("TYPEFORM_FIRST_NAME_FIELD_ID")
        self.TYPEFORM_LAST_NAME_ID = os.getenv("TYPEFORM_LAST_NAME_FIELD_ID")

        self.SLACK_API_KEY = os.getenv("SLACK_API_KEY")
        self.SLACK_HOST_NAME = os.getenv("SLACK_HOST_NAME")


class TestingConfig(Config):
    def __init__(self):
        super(TestingConfig, self).__init__()

        self.TYPEFORM_API_KEY = os.getenv("TYPEFORM_API_KEY_TEST")
        self.TYPEFORM_UID = os.getenv("TYPEFORM_UID_TEST")
        self.TYPEFORM_FIRST_NAME_ID = os.getenv("TYPEFORM_FIRST_NAME_FIELD_ID_TEST")
        self.TYPEFORM_LAST_NAME_ID = os.getenv("TYPEFORM_LAST_NAME_FIELD_ID_TEST")

        self.SLACK_API_KEY = os.getenv("SLACK_API_KEY_TEST")
        self.SLACK_HOST_NAME = os.getenv("SLACK_HOST_NAME_TEST")


config = {"production": ProductionConfig(), "testing": TestingConfig()}
