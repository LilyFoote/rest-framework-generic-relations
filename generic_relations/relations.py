from __future__ import unicode_literals

from rest_framework import serializers

from .serializers import GenericSerializerMixin


__all__ = ('GenericRelatedField',)


class GenericRelatedField(GenericSerializerMixin, serializers.Field):
    """
    Represents a generic relation / foreign key.
    It's actually more of a wrapper, that delegates the logic to registered
    serializers based on the `Model` class.
    """
