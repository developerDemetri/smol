from copy import deepcopy
from json import dumps

from flexmock import flexmock
from pynamodb.exceptions import PutError
import pytest

from smol.captcha import Captcha
from smol.exceptions import BadMethod, BadRequest, SmolError
from smol.link import Link
from smol.safe_site import SafeSite
from smol.shorten import Shortener

from tests.test_base import TestBase


class TestShortener(TestBase):
    def test_non_post(self):
        event = deepcopy(self.mock_post_event)
        event["httpMethod"] = "DELETE"

        with pytest.raises(BadMethod):
            Shortener(event)

    def test_non_json(self):
        event = deepcopy(self.mock_post_event)
        event["headers"]["content-type"] = "application/xml"

        with pytest.raises(BadRequest):
            Shortener(event)

    def test_generate_id(self):
        flexmock(Link).should_receive("get").and_raise(Link.DoesNotExist()).once()

        new_id = Shortener._generate_id()
        self.assertAlmostEqual(len(new_id), 6)

    def test_generate_id_with_collision(self):
        flexmock(Link).should_receive("get").and_return(self.mock_link).and_raise(
            Link.DoesNotExist()
        ).twice()

        new_id = Shortener._generate_id()
        self.assertAlmostEqual(len(new_id), 6)

    def test_generate_id_fails(self):
        flexmock(Link).should_receive("get").and_return(self.mock_link).times(100)

        with pytest.raises(SmolError):
            Shortener._generate_id()

    def test_shorten_link(self):
        flexmock(Captcha).should_receive("verify_captcha").with_args(
            "fakeCaptcha"
        ).and_return(True).once()
        flexmock(SafeSite).should_receive("is_safe_site").with_args(
            "https://mrteefs.com"
        ).and_return(True).once()
        flexmock(Shortener).should_receive("_generate_id").and_return("SMOLIO").once()
        flexmock(Link).should_receive("save").once()

        result = Shortener(self.mock_post_event).shorten_link()
        self.assertEqual(result.id, "SMOLIO")
        self.assertEqual(result.target, "https://mrteefs.com")

    def test_shorten_link_bad_captcha(self):
        flexmock(Captcha).should_receive("verify_captcha").with_args(
            "fakeCaptcha"
        ).and_return(False).once()

        with pytest.raises(BadRequest):
            Shortener(self.mock_post_event).shorten_link()

    def test_shorten_link_no_captcha(self):
        event = deepcopy(self.mock_post_event)
        event["body"] = dumps(
            {
                "target": "https://mrteefs.com",
            }
        )

        with pytest.raises(BadRequest):
            Shortener(event).shorten_link()

    def test_shorten_link_bad_url(self):
        event = deepcopy(self.mock_post_event)
        event["body"] = dumps(
            {
                "target": "badlink.f",
                "token": "fakeCaptcha",
            }
        )
        flexmock(Captcha).should_receive("verify_captcha").with_args(
            "fakeCaptcha"
        ).and_return(True).once()

        with pytest.raises(BadRequest):
            Shortener(event).shorten_link()

    def test_shorten_link_no_url(self):
        event = deepcopy(self.mock_post_event)
        event["body"] = dumps(
            {
                "token": "fakeCaptcha",
            }
        )
        flexmock(Captcha).should_receive("verify_captcha").with_args(
            "fakeCaptcha"
        ).and_return(True).once()

        with pytest.raises(BadRequest):
            Shortener(event).shorten_link()

    def test_shorten_link_unsafe_url(self):
        flexmock(Captcha).should_receive("verify_captcha").with_args(
            "fakeCaptcha"
        ).and_return(True).once()
        flexmock(SafeSite).should_receive("is_safe_site").with_args(
            "https://mrteefs.com"
        ).and_return(False).once()

        with pytest.raises(BadRequest):
            Shortener(self.mock_post_event).shorten_link()

    def test_shorten_link_id_race_condition(self):
        flexmock(Captcha).should_receive("verify_captcha").with_args(
            "fakeCaptcha"
        ).and_return(True).once()
        flexmock(SafeSite).should_receive("is_safe_site").with_args(
            "https://mrteefs.com"
        ).and_return(True).once()
        flexmock(Shortener).should_receive("_generate_id").and_return("SMOLIO").once()
        self.mock_conn.should_receive("put_item").and_raise(PutError()).once()

        with pytest.raises(PutError):
            Shortener(self.mock_post_event).shorten_link()

    def test_shorten_link_varying_content_type(self):
        event = deepcopy(self.mock_post_event)
        event["headers"]["content-type"] = "application/json;charset=UTF-8"
        flexmock(Captcha).should_receive("verify_captcha").with_args(
            "fakeCaptcha"
        ).and_return(True).once()
        flexmock(SafeSite).should_receive("is_safe_site").with_args(
            "https://mrteefs.com"
        ).and_return(True).once()
        flexmock(Shortener).should_receive("_generate_id").and_return("SMOLIO").once()
        flexmock(Link).should_receive("save").once()

        result = Shortener(event).shorten_link()
        self.assertEqual(result.id, "SMOLIO")
        self.assertEqual(result.target, "https://mrteefs.com")

    def test_shorten_link_bad_json(self):
        event = deepcopy(self.mock_post_event)
        event["body"] = "{'target'}"

        with pytest.raises(BadRequest):
            Shortener(event).shorten_link()
