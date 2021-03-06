import pytest
from graphene.test import Client
from pytest_factoryboy import register

from server.api.internal.schema import schema
from server.tests.factories import ShortURLFactory

for factory in (ShortURLFactory,):
    register(factory)


@pytest.fixture
def gql_client():
    return Client(schema=schema)
