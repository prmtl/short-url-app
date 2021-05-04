from django import forms
from django.db import models

import graphene
from graphene_django.converter import convert_django_field
from graphene_django.forms.converter import convert_form_field
from graphene_django.types import DjangoObjectType
from graphene_file_upload.scalars import Upload

from server.core.schema.connection import CountableConnection


class CountableDjangoObjectType(DjangoObjectType):
    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(cls, *args, **kwargs):
        # Force it to use the countable connection
        countable_conn = CountableConnection.create_type(
            "{}CountableConnection".format(cls.__name__), node=cls
        )
        super().__init_subclass_with_meta__(
            *args, connection=countable_conn, **kwargs
        )


class WithFileFields:
    @classmethod
    def __init_subclass_with_meta__(cls, *args, **kwargs):
        super().__init_subclass_with_meta__(*args, **kwargs)

        for field_name in kwargs.get("file_fields", ()):
            resolver = cls.make_file_resolver(field_name)
            setattr(cls, f"resolve_{field_name}", resolver)
            cls._meta.fields[
                field_name
            ].description = "Absolute URL to the file"

    @classmethod
    def make_file_resolver(cls, field_name):
        def resolve_file_field(root, info):
            file_field = getattr(root, field_name)
            if file_field:
                return file_field.url

        return staticmethod(resolve_file_field)


@convert_django_field.register(models.FileField)
@convert_django_field.register(models.ImageField)
def convert_model_image_field_to_string(field, registry=None):
    # NOTE(prmtl): we convert this to String since we return only URLs
    # or filename
    return graphene.String(
        description=field.help_text,
        required=(not field.null and not field.blank),
    )


@convert_form_field.register(forms.ImageField)
@convert_form_field.register(forms.FileField)
def convert_form_image_field_to_upload(field):
    return Upload(description=field.help_text, required=field.required)
