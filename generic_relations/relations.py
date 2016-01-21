from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _
from django import forms

from rest_framework.compat import six
from rest_framework.serializers import Field, ValidationError


class GenericRelatedField(Field):
    """
    Represents a generic relation foreign key.
    It's actually more of a wrapper, that delegates the logic to registered
    serializers based on the `Model` class.
    """
    default_error_messages = {
        'no_model_match': _('Invalid model - model not available.'),
        'no_url_match': _('Invalid hyperlink - No URL match'),
        'incorrect_url_match': _(
            'Invalid hyperlink - view name not available'),
    }

    form_field_class = forms.URLField

    def __init__(self, serializers, determining_errors=None, *args, **kwargs):
        """
        Needs an extra parameter `serializers` which has to be a dict
        key: value being `Model`: serializer.

        Supports a `determining_errors` parameter which is a list of
        ValidationError messages which should, in
        determine_serializer_for_data(), indicate that the respective
        serializer is not a match for the value. Default `None` means that any
        ValidationError indicates a mismatch.
        """
        super(GenericRelatedField, self).__init__(*args, **kwargs)
        self.serializers = serializers
        self.determining_errors = determining_errors
        for serializer in self.serializers.values():
            serializer.bind('', self)

    def to_internal_value(self, data):
        serializer = self.determine_serializer_for_data(data)
        return serializer.to_internal_value(data)

    def to_representation(self, instance):
        serializer = self.determine_deserializer_for_data(instance)
        return serializer.to_representation(instance)

    def determine_deserializer_for_data(self, instance):
        try:
            model = instance.__class__
            serializer = self.serializers[model]
        except KeyError:
            raise ValidationError(self.error_messages['no_model_match'])
        return serializer

    def determine_serializer_for_data(self, value):
        # While one could easily execute the "try" block within
        # to_internal_value and reduce operations, I consider the concept of
        # serializing is already very naive and vague, that's why I'd
        # go for stringency with the deserialization process here.
        serializers = []
        for serializer in six.itervalues(self.serializers):
            try:
                serializer.to_internal_value(value)
                # Collects all serializers that can handle the input data.
                serializers.append(serializer)
            except ValidationError as e:
                if self.determining_errors and e.message not in self.determining_errors:
                    # allow validation error to bubble up
                    serializers.append(serializer)
                else:
                    pass
        # If no serializer found, raise error.
        l = len(serializers)
        if l < 1:
            raise ValidationError(
                'Could not determine a valid serializer for value %r.' % value)
        elif l > 1:
            raise ValidationError(
                'There were multiple serializers found for value %r.' % value)
        return serializers[0]
