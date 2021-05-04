import logging

import graphene
from graphene import relay

from server.core.schema.types import CountableDjangoObjectType
from server.short_urls.models import ShortURL

logger = logging.getLogger(__file__)


class ShortURLType(CountableDjangoObjectType):
    hash = graphene.String(required=True)
    short = graphene.String(required=True)

    class Meta:
        model = ShortURL
        fields = ("id", "original", "hash", "created_at", "updated_at")
        interfaces = (relay.Node,)

    @staticmethod
    def resolve_hash(root, info):
        return root.hash

    @staticmethod
    def resolve_short(root, info):
        return root.short


class Query(graphene.ObjectType):
    url = relay.Node.Field(ShortURLType)
    url_by_hash = graphene.Field(
        ShortURLType, hash=graphene.String(required=True)
    )

    @staticmethod
    def resolve_url_by_hash(root, info, hash, *args, **kwargs):
        return ShortURL.objects.get_by_hash(hash)
