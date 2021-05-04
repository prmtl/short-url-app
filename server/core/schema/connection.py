import graphene
from graphene.relay.connection import Connection


class CountableConnection(Connection):
    class Meta:
        abstract = True

    total_count = graphene.Int(
        description="A total count of items in the collection."
    )

    @staticmethod
    def resolve_total_count(root, *_args, **_kwargs):
        if isinstance(root.iterable, list):
            return len(root.iterable)
        return root.iterable.count()
