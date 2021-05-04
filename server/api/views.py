import logging
import traceback

from graphene_django.views import GraphQLView as _GraphQLView
from graphene_file_upload.django import FileUploadGraphQLView
from graphql.error import GraphQLError

from server.exceptions import ServerException

logger = logging.getLogger(__name__)


class GraphQLPlaygroundMixin:
    # NOTE(prmtl): we replace GraphiQL with GraphQL Playground here
    # by using custom tempalte, so in every place we mention
    # "graphiql" we mean "graphql playground"
    graphiql_template = "graphql/graphql_playground.html"
    graphiql_version = 1.7


class GraphQLView(GraphQLPlaygroundMixin, FileUploadGraphQLView, _GraphQLView):
    @staticmethod
    def format_error(error):
        # NOTE(prmtl): it seems that in current version of graphene
        # errors are multinested so it is not enough to just get
        # error.orginial_error and we try until we can find "last one"
        original_error = get_original_error(error)
        if isinstance(original_error, ServerException):
            error.message = original_error.default_message

        if isinstance(error, GraphQLError):
            logger.exception("Error with GQL\n%s", error)

        traceback.print_tb(error.__traceback__)
        return _GraphQLView.format_error(error)


def get_original_error(error):
    while True:
        original_error = getattr(error, "original_error", None)
        if not original_error:
            return error
        error = original_error
