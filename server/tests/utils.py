def get_graphql_content(response, ignore_errors=False):
    if not ignore_errors:
        assert "errors" not in response, response["errors"]
        assert "error" not in response, response["error"]
    return response
