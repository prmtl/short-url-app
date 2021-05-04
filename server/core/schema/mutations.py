from django.core.files.base import File

import graphene
from graphene.types.utils import yank_fields_from_attrs
from graphene_django.forms.mutation import (
    BaseDjangoFormMutation,
    DjangoFormMutationOptions,
    DjangoModelFormMutation,
    ErrorType,
    fields_for_form,
)
from graphql_relay import from_global_id


class RelayMutation(graphene.relay.ClientIDMutation):
    class Meta:
        abstract = True

    errors = graphene.List(ErrorType)


class RelayModelFormMutation(DjangoModelFormMutation):
    _ID_FIELD = "id"

    class Meta:
        abstract = True

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        if cls._ID_FIELD in input:
            # NOTE(prmtl): since DjangoModelFormMutation expects
            # (due to inconsistencies in graphne-django) that
            # "id" will be actual "id", not the one provided by relay,
            # we try to decode it before passing further
            input[cls._ID_FIELD] = from_global_id(input[cls._ID_FIELD]).id
        return super().mutate_and_get_payload(root=root, info=info, **input)

    @classmethod
    def get_form_files(cls, root, info, **input):
        return {
            name: value
            for name, value in input.items()
            if isinstance(value, File)
        }

    @classmethod
    def get_form_kwargs(cls, root, info, **input):
        files = cls.get_form_files(root, info, **input)
        kwargs = {"data": input, "files": files}

        pk = input.pop("id", None)
        if pk:
            instance = cls._meta.model._default_manager.get(pk=pk)
            kwargs["instance"] = instance

        return kwargs

    @classmethod
    def update_related(cls, root, info, form_class, parent_field, input):
        model_class = form_class._meta.model

        all_forms = []
        updated_pks = set()
        errors = []

        if parent_field not in input:
            return errors

        input_items = input[parent_field]

        for item_idx, data in enumerate(input_items):
            files = cls.get_form_files(root=root, info=info, **data)
            form_kwargs = {"data": data, "files": files}
            encoded_id = data.pop("id", None)

            if encoded_id:
                pk = from_global_id(encoded_id).id
                instance = model_class.objects.get(pk=pk)
                form_kwargs["instance"] = instance
                updated_pks.add(pk)

            form = form_class(**form_kwargs)
            all_forms.append(form)

            if not form.is_valid():
                prefixed_errors = {
                    f"{parent_field}.{item_idx}.{field}": value
                    for field, value in form.errors.items()
                }
                errors.extend(ErrorType.from_errors(prefixed_errors))

        if not errors:
            model_class.objects.exclude(pk__in=updated_pks).delete()

            for form in all_forms:
                form.save()

        return errors


class RelayFormMutation(BaseDjangoFormMutation):
    """Form mutation that do not return entered fields as DjangoFormMutation
    is doing.
    """

    class Meta:
        abstract = True

    errors = graphene.List(ErrorType)

    @classmethod
    def __init_subclass_with_meta__(
        cls, form_class=None, only_fields=(), exclude_fields=(), **options
    ):

        if not form_class:
            raise Exception("form_class is required for RelayFormMutation")

        form = form_class()
        input_fields = fields_for_form(form, only_fields, exclude_fields)

        _meta = DjangoFormMutationOptions(cls)
        _meta.form_class = form_class

        input_fields = yank_fields_from_attrs(
            input_fields, _as=graphene.InputField
        )
        super().__init_subclass_with_meta__(
            _meta=_meta, input_fields=input_fields, **options
        )

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        form = cls.get_form(root, info, **input)

        if form.is_valid():
            return cls.perform_mutate(form, info)
        else:
            errors = ErrorType.from_errors(form.errors)
            return cls(errors=errors)

    @classmethod
    def perform_mutate(cls, form, info):
        return cls(errors=[])
