import graphene


class Query(
    graphene.ObjectType,
):
    ping = graphene.String()

    @staticmethod
    def resolve_ping(root, info):
        return "pong"


# class Mutation(
#     graphene.ObjectType,
# ):
#     pass


schema = graphene.Schema(
    query=Query,
    # mutation=Mutation
)
