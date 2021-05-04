from server.tests.utils import get_graphql_content


def test_ping_pong(gql_client):
    query = """
        query {
            ping
        }
        """
    response = gql_client.execute(query)
    content = get_graphql_content(response)
    assert content == {"data": {"ping": "pong"}}
