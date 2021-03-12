from flexmock import flexmock
import requests

from smol.captcha import Captcha, CAPTCHA_KEY

from tests.test_base import TestBase


class TestCaptcha(TestBase):

    token = "mock"

    def test_verify_captcha(self):
        mock_resp = flexmock()
        mock_resp.should_receive("raise_for_status").once()
        mock_resp.should_receive("json").and_return(
            {"success": True, "score": 1.0}
        ).once()
        flexmock(requests).should_receive("post").with_args(
            "https://www.google.com/recaptcha/api/siteverify",
            data={"secret": CAPTCHA_KEY, "response": self.token},
        ).and_return(mock_resp).once()

        self.assertTrue(Captcha.verify_captcha(self.token))

    def test_verify_captcha_no_token(self):
        self.assertFalse(Captcha.verify_captcha(None))

    def test_verify_captcha_fails(self):
        mock_resp = flexmock()
        mock_resp.should_receive("raise_for_status").once()
        mock_resp.should_receive("json").and_return(
            {"success": False, "score": 0.0}
        ).once()
        flexmock(requests).should_receive("post").with_args(
            "https://www.google.com/recaptcha/api/siteverify",
            data={"secret": CAPTCHA_KEY, "response": self.token},
        ).and_return(mock_resp).once()

        self.assertFalse(Captcha.verify_captcha(self.token))

    def test_verify_captcha_errors(self):
        mock_resp = flexmock()
        mock_resp.should_receive("raise_for_status").and_raise(
            requests.exceptions.HTTPError()
        ).once()
        flexmock(requests).should_receive("post").with_args(
            "https://www.google.com/recaptcha/api/siteverify",
            data={"secret": CAPTCHA_KEY, "response": self.token},
        ).and_return(mock_resp).once()

        self.assertFalse(Captcha.verify_captcha(self.token))
