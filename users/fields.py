from collections import OrderedDict

from rest_framework import serializers


class ShowDetailsAcceptPkField(serializers.PrimaryKeyRelatedField):
    """
    This field shows details (on GET) but accepts pk identifiers (on POST)
    Adapted from https://github.com/encode/django-rest-framework/issues/5206#issue-234442095
    """

    def __init__(self, serializer, **kwargs):
        super().__init__(**kwargs)
        self.serializer_class = serializer

    def to_representation(self, value):
        return self.serializer_class(value, context=self.context, **self._kwargs).data

    def get_queryset(self):
        if self.queryset:
            return self.queryset
        return self.serializer_class.Meta.model.objects.all()

    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            return {}

        if cutoff is not None:
            queryset = queryset[:cutoff]

        return OrderedDict([
            (
                item.pk,
                self.display_value(item)
            )
            for item in queryset
        ])

    def use_pk_only_optimization(self):
        return False
