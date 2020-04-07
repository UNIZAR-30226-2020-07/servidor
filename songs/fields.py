from rest_framework.fields import IntegerField

from users.models import Valoration


class ValorationField(IntegerField):
    """
    For Song valorations
    """

    def __init__(self, **kwargs):
        kwargs['source'] = '*'  # this indicates that the field should return the whole object
        kwargs['validators'] = Valoration.valoration.field.validators
        super().__init__(**kwargs)

    def to_representation(self, song):
        user = self.context['request'].user
        if user.is_authenticated:
            query = Valoration.objects.filter(user=user, song=song)
            if query.exists():
                # get the valoration of a registered user, if exists
                return query.get().valoration

    def to_internal_value(self, valoration):
        # the partial song
        return {self.field_name: super().to_internal_value(valoration)}

    def run_validators(self, song):
        # validates the valoration
        super().run_validators(song[self.field_name])
