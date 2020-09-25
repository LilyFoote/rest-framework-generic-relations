from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _
from django import forms

from rest_framework import serializers


__all__ = ('GenericSerializerMixin', 'GenericModelSerializer',)


class GenericSerializerMixin(object):
    default_error_messages = {
        'no_model_match': _('Invalid model - model not available.'),
        'no_url_match': _('Invalid hyperlink - No URL match'),
        'incorrect_url_match': _(
            'Invalid hyperlink - view name not available'),
    }

    form_field_class = forms.URLField

    def __init__(self, serializers, *args, **kwargs):
        """
        Needs an extra parameter `serializers` which has to be a dict
        key: value being `Model`: serializer.
        """
        super(GenericSerializerMixin, self).__init__(*args, **kwargs)
        self.serializers = serializers
        for serializer in self.serializers.values():
            if serializer.source is not None:
                msg = '{}() cannot be re-used. Create a new instance.'
                raise RuntimeError(msg.format(type(serializer).__name__))
            serializer.bind('', self)

    def to_internal_value(self, data):
        try:
            serializer = self.get_deserializer_for_data(data)
        except ImproperlyConfigured as e:
            raise serializers.ValidationError(e)
        return serializer.to_internal_value(data)

    def to_representation(self, instance):
        serializer = self.get_serializer_for_instance(instance)
        return serializer.to_representation(instance)

    def get_serializer_for_instance(self, instance):
        # Use registered superclasses, rather than only the exact model.
        # (But prefer things earlier in the MRO, so if the exact model is registered,
        # use that in preference to any superclasses)
        for klass in instance.__class__.mro():
            if klass in self.serializers:
                return self.serializers[klass]

        raise serializers.ValidationError(self.error_messages['no_model_match'])

    def get_deserializer_for_data(self, value):
        # While one could easily execute the "try" block within
        # to_internal_value and reduce operations, I consider the concept of
        # serializing is already very naive and vague, that's why I'd
        # go for stringency with the deserialization process here.
        serializers = []
        for serializer in self.serializers.values():
            try:
                serializer.to_internal_value(value)
                # Collects all serializers that can handle the input data.
                serializers.append(serializer)
            except Exception:
                pass
        # If no serializer found, raise error.
        l = len(serializers)
        if l < 1:
            raise ImproperlyConfigured(
                'Could not determine a valid serializer for value %r.' % value)
        elif l > 1:
            raise ImproperlyConfigured(
                'There were multiple serializers found for value %r.' % value)
        return serializers[0]


class GenericModelSerializer(GenericSerializerMixin, serializers.Serializer):
    """
    Delegates serialization and deserialization to registered serializers
    based on the type of the model.
    """
