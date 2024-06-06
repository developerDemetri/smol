import pytest
from flexmock import flexmock

from smol.exceptions import BadMethod, BadRequest, LinkNotFound
from smol.link import Link
from smol.models import LambdaRequest
from smol.resolve import Resolver

from tests.test_base import TestBase


class TestResolver(TestBase):
    def test_non_get(self):
        req = LambdaRequest(headers={}, method="DELETE", path="smolio", body="")

        with pytest.raises(BadMethod):
            Resolver(req)

    def test_resolve_link(self):
        req = LambdaRequest(headers={}, method="GET", path="smolio", body="")
        flexmock(Link).should_receive("get").with_args("SMOLIO").and_return(
            self.mock_link
        ).once()

        result = Resolver(req).resolve_link()
        self.assertEqual(result.id, "SMOLIO")
        self.assertEqual(result.target, "https://mrteefs.com")

    def test_resolve_link_bad_link(self):
        req = LambdaRequest(headers={}, method="GET", path="/n0pe___", body="")

        with pytest.raises(BadRequest):
            Resolver(req).resolve_link()

    def test_resolve_link_not_found(self):
        req = LambdaRequest(headers={}, method="GET", path="smolio", body="")
        flexmock(Link).should_receive("get").with_args("SMOLIO").and_raise(
            Link.DoesNotExist()
        ).once()

        with pytest.raises(LinkNotFound):
            Resolver(req).resolve_link()
