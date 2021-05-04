import graphene

from server.short_urls.schema import Mutation as ShortURLsMutation
from server.short_urls.schema import Query as ShortURLsQuery


class Query(
    ShortURLsQuery,
    graphene.ObjectType,
):
    ping = graphene.String()

    @staticmethod
    def resolve_ping(root, info):
        return "pong"


class Mutation(
    ShortURLsMutation,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
