import logging

import graphene
from graphene import relay

from server.core.schema.mutations import RelayModelFormMutation
from server.core.schema.types import CountableDjangoObjectType
from server.short_urls.forms import ShortURLForm
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


class CreateShortUrlMutation(RelayModelFormMutation):
    short_url = graphene.Field(ShortURLType)

    class Meta:
        form_class = ShortURLForm
        exclude_fields = ("id",)


class Query(graphene.ObjectType):
    url = relay.Node.Field(ShortURLType)
    url_by_hash = graphene.Field(
        ShortURLType, hash=graphene.String(required=True)
    )

    @staticmethod
    def resolve_url_by_hash(root, info, hash, *args, **kwargs):
        return ShortURL.objects.get_by_hash(hash)


class Mutation(graphene.ObjectType):
    create_short_url = CreateShortUrlMutation.Field()
