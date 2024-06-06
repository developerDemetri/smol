from json import dumps
from os import environ
from unittest import TestCase

from flexmock import flexmock
from flexmock._api import flexmock_teardown

from smol.link import Link


class TestBase(TestCase):
    mock_link = Link(id="SMOLIO", target="https://mrteefs.com")
    mock_get_event = {
        "version": "2.0",
        "routeKey": "$default",
        "rawPath": "/smolio",
        "rawQueryString": "",
        "headers": {
            "content-length": "25",
            "x-amzn-tls-version": "TLSv1.3",
            "x-forwarded-proto": "https",
            "x-forwarded-port": "443",
            "x-forwarded-for": "89.98.233.85",
            "accept": "*/*",
            "x-amzn-tls-cipher-suite": "TLS_AES_128_GCM_SHA256",
            "x-amzn-trace-id": "Root=1-6661bc42-0cfc3dba4ac557d9102d6107",
            "host": "xxw3qkqlfjfeg4ugoisqa64eae0trlpq.lambda-url.eu-west-1.on.aws",
            "content-type": "application/json",
            "cache-control": "no-cache",
            "accept-encoding": "gzip, deflate, br",
            "user-agent": "PostmanRuntime/7.39.0",
        },
        "requestContext": {
            "accountId": "anonymous",
            "apiId": "xxw3qkqlfjfeg4ugoisqa64eae0trlpq",
            "domainName": "xxw3qkqlfjfeg4ugoisqa64eae0trlpq.lambda-url.eu-west-1.on.aws",
            "domainPrefix": "xxw3qkqlfjfeg4ugoisqa64eae0trlpq",
            "http": {
                "method": "GET",
                "path": "/smolio",
                "protocol": "HTTP/1.1",
                "sourceIp": "89.98.233.85",
                "userAgent": "PostmanRuntime/7.39.0",
            },
            "requestId": "1e9a1dc2-22a2-4dff-94f8-de880577d938",
            "routeKey": "$default",
            "stage": "$default",
            "time": "06/Jun/2024:13:40:18 +0000",
            "timeEpoch": 1717681218529,
        },
        "body": "",
        "isBase64Encoded": False,
    }

    mock_post_event = {
        "version": "2.0",
        "routeKey": "$default",
        "rawPath": "/api/v1/link",
        "rawQueryString": "",
        "headers": {
            "content-length": "25",
            "x-amzn-tls-version": "TLSv1.3",
            "x-forwarded-proto": "https",
            "x-forwarded-port": "443",
            "x-forwarded-for": "89.98.233.85",
            "accept": "*/*",
            "x-amzn-tls-cipher-suite": "TLS_AES_128_GCM_SHA256",
            "x-amzn-trace-id": "Root=1-6661bc42-0cfc3dba4ac557d9102d6107",
            "host": "xxw3qkqlfjfeg4ugoisqa64eae0trlpq.lambda-url.eu-west-1.on.aws",
            "content-type": "application/json",
            "cache-control": "no-cache",
            "accept-encoding": "gzip, deflate, br",
            "user-agent": "PostmanRuntime/7.39.0",
        },
        "requestContext": {
            "accountId": "anonymous",
            "apiId": "xxw3qkqlfjfeg4ugoisqa64eae0trlpq",
            "domainName": "xxw3qkqlfjfeg4ugoisqa64eae0trlpq.lambda-url.eu-west-1.on.aws",
            "domainPrefix": "xxw3qkqlfjfeg4ugoisqa64eae0trlpq",
            "http": {
                "method": "POST",
                "path": "/api/v1/link",
                "protocol": "HTTP/1.1",
                "sourceIp": "89.98.233.85",
                "userAgent": "PostmanRuntime/7.39.0",
            },
            "requestId": "1e9a1dc2-22a2-4dff-94f8-de880577d938",
            "routeKey": "$default",
            "stage": "$default",
            "time": "06/Jun/2024:13:40:18 +0000",
            "timeEpoch": 1717681218529,
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
