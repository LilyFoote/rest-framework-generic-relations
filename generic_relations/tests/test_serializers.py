

from django.test import TestCase

from rest_framework import serializers

from generic_relations.serializers import GenericModelSerializer
from generic_relations.tests.models import Bookmark, Note

from .test_relations import BookmarkSerializer, NoteSerializer


class TestGenericModelSerializer(TestCase):
    def setUp(self):
        self.bookmark = Bookmark.objects.create(
            url='https://www.djangoproject.com/')
        self.note = Note.objects.create(text='Remember the milk')
        self.note2 = Note.objects.create(text='Reticulate the splines')

        self.serializer = GenericModelSerializer(
            {
                Bookmark: BookmarkSerializer(),
                Note: NoteSerializer(),
            }
        )
        self.list_serializer = serializers.ListSerializer(child=self.serializer)

    def test_serialize(self):
        self.assertEqual(
            self.serializer.to_representation(self.bookmark),
            {'url': 'https://www.djangoproject.com/'},
        )
        self.assertEqual(
            self.serializer.to_representation(self.note),
            {'text': 'Remember the milk'},
        )

    def test_deserialize(self):
        self.assertEqual(
            self.serializer.to_internal_value({'url': 'https://www.djangoproject.com/'}),
            {'url': 'https://www.djangoproject.com/'},
        )
        self.assertEqual(
            self.serializer.to_internal_value({'text': 'Remember the milk'}),
            {'text': 'Remember the milk'},
        )

    def test_serialize_list(self):
        actual = self.list_serializer.to_representation([
            self.bookmark, self.note, self.note2, self.bookmark,
        ])
        expected = [
            {'url': 'https://www.djangoproject.com/'},
            {'text': 'Remember the milk'},
            {'text': 'Reticulate the splines'},
            {'url': 'https://www.djangoproject.com/'},
        ]
        self.assertEqual(actual, expected)

    def test_deserialize_list(self):
        validated_data = self.list_serializer.to_internal_value([
            {'url': 'https://www.djangoproject.com/'},
            {'text': 'Remember the milk'},
            {'text': 'Reticulate the splines'},
            {'url': 'https://www.djangoproject.com/'},
        ])

        self.assertEqual(validated_data, [
            {'url': 'https://www.djangoproject.com/'},
            {'text': 'Remember the milk'},
            {'text': 'Reticulate the splines'},
            {'url': 'https://www.djangoproject.com/'},
        ])
