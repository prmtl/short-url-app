import pytest

from server.tests.utils import get_graphql_content


@pytest.fixture(autouse=True)
def setup_domains(settings):
    settings.SHORT_URL_DOMAIN_NAME = "shorturl.local"
    settings.SHORT_URL_SCHEME = "https"


def test_get_url_by_hash(db, short_url, gql_client):
    query = """
        query getShortUrlByHash($hash: String!) {
            urlByHash(hash: $hash) {
                    id
                    original
                    short
                    hash
                }
        }
        """
    variables = {"hash": short_url.hash}
    response = gql_client.execute(query, variables=variables)
    content = get_graphql_content(response)
    data = content["data"]["urlByHash"]
    assert data["hash"] == short_url.hash
    assert data["original"] == short_url.original
    assert data["short"] == f"https://shorturl.local/{short_url.hash}"


def test_create_short_url(db, gql_client):
    mutation = """
        mutation createShortUrl($input: CreateShortUrlMutationInput!) {
            createShortUrl(input: $input) {
                shortURL {
                    id
                    original
                    short
                    hash
                }
                errors {
                  field
                  messages
                }
            }
        }
        """

    input_data = {"original": "http://google.pl/path1?param2=3"}
    variables = {"input": input_data}
    response = gql_client.execute(mutation, variables=variables)
    content = get_graphql_content(response)

    data = content["data"]["createShortUrl"]["shortURL"]
    assert data["original"] == input_data["original"]
    assert data["short"] == f"https://shorturl.local/{data['hash']}"
