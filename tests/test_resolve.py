from copy import deepcopy

import pytest
from flexmock import flexmock

from smol.exceptions import BadMethod, BadRequest, LinkNotFound
from smol.link import Link
from smol.resolve import Resolver

from tests.test_base import TestBase


class TestResolver(TestBase):
    def test_non_get(self):
        event = deepcopy(self.mock_get_event)
        event["httpMethod"] = "DELETE"

        with pytest.raises(BadMethod):
            Resolver(event)

    def test_resolve_link(self):
        flexmock(Link).should_receive("get").with_args("SMOLIO").and_return(
            self.mock_link
        ).once()

        result = Resolver(self.mock_get_event).resolve_link()
        self.assertEqual(result.id, "SMOLIO")
        self.assertEqual(result.target, "https://mrteefs.com")

    def test_resolve_link_bad_link(self):
        event = deepcopy(self.mock_get_event)
        event["path"] = "/n0pe___"

        with pytest.raises(BadRequest):
            Resolver(event).resolve_link()

    def test_resolve_link_not_found(self):
        flexmock(Link).should_receive("get").with_args("SMOLIO").and_raise(
            Link.DoesNotExist()
        ).once()

        with pytest.raises(LinkNotFound):
            Resolver(self.mock_get_event).resolve_link()
