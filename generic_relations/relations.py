from __future__ import unicode_literals

from django.utils.deprecation import RenameMethodsBase

from rest_framework.compat import six
from rest_framework import serializers

from .serializers import GenericSerializerMixin


__all__ = ('GenericRelatedField',)


class RenamedMethods(RenameMethodsBase):
    renamed_methods = (
        ('determine_deserializer_for_data', 'get_serializer_for_instance', DeprecationWarning),
        ('determine_serializer_for_data', 'get_deserializer_for_data', DeprecationWarning),
    )


class GenericRelatedField(six.with_metaclass(RenamedMethods, GenericSerializerMixin, serializers.Field)):
    """
    Represents a generic relation / foreign key.
    It's actually more of a wrapper, that delegates the logic to registered
    serializers based on the `Model` class.
    """

