from copy import deepcopy
from json import dumps

from flexmock import flexmock

from smol import api
from smol.exceptions import BadRequest, LinkNotFound
from smol.resolve import Resolver
from smol.shorten import Shortener

from tests.test_base import TestBase


class TestApi(TestBase):
    def test_http_handler_options(self):
        event = deepcopy(self.mock_post_event)
        event["requestContext"]["http"]["method"] = "OPTIONS"

        resp = api.http_handler(event, None)
        self.assertDictEqual(
            resp,
            dict(
                statusCode=200,
                statusDescription="200 OK",
                headers={
                    "access-control-allow-origin": "https://smol.io",
                    "access-control-allow-methods": "POST, GET, OPTIONS",
                    "content-type": "application/json",
                    "strict-transport-security": "max-age=31536000; includeSubDomains; preload",
                    "x-xss-protection": "1; mode=block",
                },
                body="{}",
            ),
        )

    def test_http_handler_shorten(self):
        flexmock(Shortener).should_receive("shorten_link").with_args().and_return(
            self.mock_link
        ).once()

        resp = api.http_handler(self.mock_post_event, None)
        self.assertDictEqual(
            resp,
            dict(
                statusCode=201,
                statusDescription="201 Created",
                headers={
                    "access-control-allow-origin": "https://smol.io",
                    "access-control-allow-methods": "POST, GET, OPTIONS",
                    "content-type": "application/json",
                    "strict-transport-security": "max-age=31536000; includeSubDomains; preload",
                    "x-xss-protection": "1; mode=block",
                },
                body=dumps({"id": "SMOLIO", "target": "https://mrteefs.com"}),
            ),
        )

    def test_http_handler_resolve(self):
        flexmock(Resolver).should_receive("resolve_link").with_args().and_return(
            self.mock_link
        ).once()

        resp = api.http_handler(self.mock_get_event, None)
        self.assertDictEqual(
            resp,
            dict(
                statusCode=301,
                statusDescription="301 Moved Permanently",
                headers={
                    "access-control-allow-origin": "https://smol.io",
                    "access-control-allow-methods": "POST, GET, OPTIONS",
                    "location": "https://mrteefs.com",
                    "content-type": "application/json",
                    "strict-transport-security": "max-age=31536000; includeSubDomains; preload",
                    "x-xss-protection": "1; mode=block",
                },
                body="{}",
            ),
        )

    def test_http_handler_resolve_missing(self):
        flexmock(Resolver).should_receive("resolve_link").with_args().and_raise(
            LinkNotFound()
        ).once()

        resp = api.http_handler(self.mock_get_event, None)
        self.assertDictEqual(
            resp,
            dict(
                statusCode=301,
                statusDescription="301 Moved Permanently",
                headers={
                    "access-control-allow-origin": "https://smol.io",
                    "access-control-allow-methods": "POST, GET, OPTIONS",
                    "location": "https://smol.io/?im=lost",
                    "content-type": "application/json",
                    "strict-transport-security": "max-age=31536000; includeSubDomains; preload",
                    "x-xss-protection": "1; mode=block",
                },
                body=dumps(
                    {
                        "message": "Link Not Found",
                    }
                ),
            ),
        )

    def test_http_handler_smol_err(self):
        flexmock(Shortener).should_receive("shorten_link").with_args().and_raise(
            BadRequest()
        ).once()

        resp = api.http_handler(self.mock_post_event, None)
        self.assertDictEqual(
            resp,
            dict(
                statusCode=400,
                statusDescription="400 Bad Request",
                headers={
                    "access-control-allow-origin": "https://smol.io",
                    "access-control-allow-methods": "POST, GET, OPTIONS",
                    "content-type": "application/json",
                    "strict-transport-security": "max-age=31536000; includeSubDomains; preload",
                    "x-xss-protection": "1; mode=block",
                },
                body=dumps({"message": "Invalid Request"}),
            ),
        )

    def test_http_handler_uncaught_err(self):
        flexmock(Shortener).should_receive("shorten_link").with_args().and_raise(
            RuntimeError()
        ).once()

        resp = api.http_handler(self.mock_post_event, None)
        self.assertDictEqual(
            resp,
            dict(
                statusCode=500,
                statusDescription="500 Internal Server Error",
                headers={
                    "access-control-allow-origin": "https://smol.io",
                    "access-control-allow-methods": "POST, GET, OPTIONS",
                    "content-type": "application/json",
                    "strict-transport-security": "max-age=31536000; includeSubDomains; preload",
                    "x-xss-protection": "1; mode=block",
                },
                body=dumps({"message": "Something broke :/"}),
            ),
        )
