from flexmock import flexmock
import requests

from smol.safe_site import SafeSite, SAFE_BROWSING_URI, THREATS

from tests.test_base import TestBase


class TestSafeSite(TestBase):
    site = "https://mrteefs.com"

    def test_is_safe_site(self):
        mock_resp = flexmock()
        mock_resp.should_receive("raise_for_status").once()
        mock_resp.should_receive("json").and_return(dict()).once()
        flexmock(requests).should_receive("post").with_args(
            SAFE_BROWSING_URI,
            json={
                "client": {"clientId": "smol.io"},
                "threatInfo": {
                    "threatTypes": THREATS,
                    "platformTypes": ["ANY_PLATFORM"],
                    "threatEntryTypes": ["URL"],
                    "threatEntries": [
                        {"url": self.site},
                    ],
                },
            },
        ).and_return(mock_resp).once()

        self.assertTrue(SafeSite.is_safe_site(self.site))

    def test_is_not_safe_site(self):
        mock_resp = flexmock()
        mock_resp.should_receive("raise_for_status").once()
        mock_resp.should_receive("json").and_return(
            {
                "matches": [
                    {
                        "threatType": "MALWARE",
                        "platformType": "ANY_PLATFORM",
                        "threat": {"url": self.site},
                        "cacheDuration": "300s",
                        "threatEntryType": "URL",
                    }
                ]
            }
        ).once()
        flexmock(requests).should_receive("post").with_args(
            SAFE_BROWSING_URI,
            json={
                "client": {"clientId": "smol.io"},
                "threatInfo": {
                    "threatTypes": THREATS,
                    "platformTypes": ["ANY_PLATFORM"],
                    "threatEntryTypes": ["URL"],
                    "threatEntries": [
                        {"url": self.site},
                    ],
                },
            },
        ).and_return(mock_resp).once()

        self.assertFalse(SafeSite.is_safe_site(self.site))

    def test_is_safe_site_errors(self):
        mock_resp = flexmock()
        mock_resp.should_receive("raise_for_status").and_raise(
            requests.exceptions.HTTPError()
        ).once()
        flexmock(requests).should_receive("post").with_args(
            SAFE_BROWSING_URI,
            json={
                "client": {"clientId": "smol.io"},
                "threatInfo": {
                    "threatTypes": THREATS,
                    "platformTypes": ["ANY_PLATFORM"],
                    "threatEntryTypes": ["URL"],
                    "threatEntries": [
                        {"url": self.site},
                    ],
                },
            },
        ).and_return(mock_resp).once()

        self.assertFalse(SafeSite.is_safe_site(self.site))
