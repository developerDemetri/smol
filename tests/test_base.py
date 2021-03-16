from json import dumps
from os import environ
from unittest import TestCase

from flexmock import flexmock, flexmock_teardown

from smol.link import Link


class TestBase(TestCase):

    mock_link = Link(id="SMOLIO", target="https://mrteefs.com")
    mock_get_event = {
        "requestContext": {
            "elb": {
                "targetGroupArn": "arn:aws:elasticloadbalancing:eu-west-1:012345678901:targetgroup/mock/testing123"
            }
        },
        "httpMethod": "GET",
        "path": "/smolio",
        "queryStringParameters": {},
        "headers": {
            "accept": "*/*",
            "accept-encoding": "gzip",
            "accept-language": "en-US",
            "connection": "keep-alive",
            "cookie": "",
            "host": "smol.io",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:60.0) Gecko/20100101 Firefox/60.0",
            "x-amzn-trace-id": "Root=1-5bdb40ca-556d8b0c50dc66f0511bf520",
            "x-forwarded-for": "192.0.2.1",
            "x-forwarded-port": "443",
            "x-forwarded-proto": "https",
        },
        "body": dumps(dict()),
        "isBase64Encoded": False,
    }
    mock_post_event = {
        "requestContext": {
            "elb": {
                "targetGroupArn": "arn:aws:elasticloadbalancing:eu-west-1:012345678901:targetgroup/mock/testing123"
            }
        },
        "httpMethod": "POST",
        "path": "/api/v1/link",
        "queryStringParameters": {},
        "headers": {
            "accept": "*/*",
            "accept-encoding": "gzip",
            "accept-language": "en-US",
            "connection": "keep-alive",
            "content-type": "application/json",
            "cookie": "",
            "host": "smol.io",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:60.0) Gecko/20100101 Firefox/60.0",
            "x-amzn-trace-id": "Root=1-5bdb40ca-556d8b0c50dc66f0511bf520",
            "x-forwarded-for": "192.0.2.1",
            "x-forwarded-port": "443",
            "x-forwarded-proto": "https",
        },
        "body": dumps(
            {
                "target": "https://mrteefs.com",
                "token": "fakeCaptcha",
            }
        ),
        "isBase64Encoded": False,
    }

    @classmethod
    def setUpClass(cls):
        environ["AWS_ACCESS_KEY_ID"] = "mock"
        environ["AWS_SECRET_ACCESS_KEY"] = "mock"
        environ["CAPTCHA_KEY"] = "mock"
        environ["SAFE_BROWSING_KEY"] = "mock"

    def setUp(self) -> None:
        super().setUp()
        self.mock_conn = flexmock()
        flexmock(Link).should_receive("_get_connection").and_return(self.mock_conn)

    def tearDown(self) -> None:
        flexmock_teardown()
        return super().tearDown()
