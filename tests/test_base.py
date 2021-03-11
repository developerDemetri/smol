from os import environ
from unittest import TestCase

from flexmock import flexmock_teardown


class TestBase(TestCase):
    @classmethod
    def setUpClass(cls):
        environ["AWS_ACCESS_KEY_ID"] = "mock"
        environ["AWS_SECRET_ACCESS_KEY"] = "mock"
        environ["CAPTCHA_KEY"] = "mock"

    def tearDown(self) -> None:
        flexmock_teardown()
        return super().tearDown()
