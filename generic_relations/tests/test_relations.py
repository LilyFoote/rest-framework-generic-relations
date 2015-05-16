from __future__ import unicode_literals
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.test import TestCase, RequestFactory
from rest_framework import serializers
try:
    from django.conf.urls import url
except ImportError:
    from django.conf.urls.defaults import url

from rest_framework.reverse import reverse

from generic_relations.relations import GenericRelatedField
from generic_relations.tests.models import Bookmark, Detachable, Note, Tag


factory = RequestFactory()
# Just to ensure we have a request in the serializer context
request = factory.get('/')


def dummy_view(request, pk):
    pass

urlpatterns = [
    url(r'^bookmark/(?P<pk>[0-9]+)/$', dummy_view, name='bookmark-detail'),
    url(r'^detachable/(?P<pk>[0-9]+)/$', dummy_view, name='detachable-detail'),
    url(r'^note/(?P<pk>[0-9]+)/$', dummy_view, name='note-detail'),
    url(r'^tag/(?P<pk>[0-9]+)/$', dummy_view, name='tag-detail'),
    url(
        r'^contact/(?P<my_own_slug>[-\w]+)/$',
        dummy_view,
        name='contact-detail'
    ),
]


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        exclude = ('id', )


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        exclude = ('id', )


class TestGenericRelatedFieldDeserialization(TestCase):

    urls = 'generic_relations.tests.test_relations'

    def setUp(self):
        self.bookmark = Bookmark.objects.create(
            url='https://www.djangoproject.com/')
        Tag.objects.create(tagged_item=self.bookmark, tag='django')
        Tag.objects.create(tagged_item=self.bookmark, tag='python')
        self.note = Note.objects.create(text='Remember the milk')
        Tag.objects.create(tagged_item=self.note, tag='reminder')

        Detachable.objects.create(content_object=self.note, name='attached')
        Detachable.objects.create(name='detached')

    def test_relations_as_hyperlinks(self):

        class TagSerializer(serializers.ModelSerializer):
            tagged_item = GenericRelatedField(
                {
                    Bookmark: serializers.HyperlinkedRelatedField(
                        view_name='bookmark-detail'),
                    Note: serializers.HyperlinkedRelatedField(
                        view_name='note-detail'),
                },
                source='tagged_item',
                read_only=True,
            )

            class Meta:
                model = Tag
                exclude = ('id', 'content_type', 'object_id', )

        serializer = TagSerializer(Tag.objects.all(), many=True, context={'request': request})
        expected = [
            {
                'tagged_item': 'http://testserver/bookmark/1/',
                'tag': 'django',
            },
            {
                'tagged_item': 'http://testserver/bookmark/1/',
                'tag': 'python',
            },
            {
                'tagged_item': 'http://testserver/note/1/',
                'tag': 'reminder'
            }
        ]
        self.assertEqual(serializer.data, expected)

    def test_relations_as_nested(self):

        class TagSerializer(serializers.ModelSerializer):
            tagged_item = GenericRelatedField({
                Bookmark: BookmarkSerializer(),
                Note: NoteSerializer(),
            }, source='tagged_item', read_only=True)

            class Meta:
                model = Tag
                exclude = ('id', 'content_type', 'object_id', )

        serializer = TagSerializer(Tag.objects.all(), many=True)
        expected = [
            {
                'tagged_item': {
                    'url': 'https://www.djangoproject.com/'
                },
                'tag': 'django'
            },
            {
                'tagged_item': {
                    'url': 'https://www.djangoproject.com/'
                },
                'tag': 'python'
            },
            {
                'tagged_item': {
                    'text': 'Remember the milk',
                },
                'tag': 'reminder'
            }
        ]
        self.assertEqual(serializer.data, expected)

    def test_mixed_serializers(self):
        class TagSerializer(serializers.ModelSerializer):
            tagged_item = GenericRelatedField(
                {
                    Bookmark: BookmarkSerializer(),
                    Note: serializers.HyperlinkedRelatedField(
                        view_name='note-detail'),
                },
                source='tagged_item',
                read_only=True,
            )

            class Meta:
                model = Tag
                exclude = ('id', 'content_type', 'object_id', )

        serializer = TagSerializer(Tag.objects.all(), many=True, context={'request': request})
        expected = [
            {
                'tagged_item': {
                    'url': 'https://www.djangoproject.com/'
                },
                'tag': 'django'
            },
            {
                'tagged_item': {
                    'url': 'https://www.djangoproject.com/'
                },
                'tag': 'python'
            },
            {
                'tagged_item': 'http://testserver/note/1/',
                'tag': 'reminder'
            }
        ]
        self.assertEqual(serializer.data, expected)

    def test_invalid_model(self):
        # Leaving out the Note model should result in a ValidationError
        class TagSerializer(serializers.ModelSerializer):
            tagged_item = GenericRelatedField({
                Bookmark: BookmarkSerializer(),
            }, source='tagged_item', read_only=True)

            class Meta:
                model = Tag
                exclude = ('id', 'content_type', 'object_id', )
        serializer = TagSerializer(Tag.objects.all(), many=True)

        def call_data():
            return serializer.data
        self.assertRaises(ValidationError, call_data)

    def test_relation_as_null(self):
        class DetachableSerializer(serializers.ModelSerializer):
            content_object = GenericRelatedField(
                {
                    Bookmark: serializers.HyperlinkedRelatedField(
                        view_name='bookmark-detail'),
                    Note: serializers.HyperlinkedRelatedField(
                        view_name='note-detail'),
                },
                source='content_object',
                read_only=True,
            )

            class Meta:
                model = Detachable
                exclude = ('id', 'content_type', 'object_id', )

        serializer = DetachableSerializer(Detachable.objects.all(), many=True, context={'request': request})
        expected = [
            {
                'content_object': 'http://testserver/note/1/',
                'name': 'attached',
            },
            {
                'content_object': None,
                'name': 'detached',
            }
        ]
        self.assertEqual(serializer.data, expected)


class TestGenericRelatedFieldSerialization(TestCase):

    urls = 'generic_relations.tests.test_relations'

    def setUp(self):
        self.bookmark = Bookmark.objects.create(
            url='https://www.djangoproject.com/')
        Tag.objects.create(tagged_item=self.bookmark, tag='django')
        Tag.objects.create(tagged_item=self.bookmark, tag='python')
        self.note = Note.objects.create(text='Remember the milk')

    def test_hyperlink_serialization(self):
        class TagSerializer(serializers.ModelSerializer):
            tagged_item = GenericRelatedField(
                {
                    Bookmark: serializers.HyperlinkedRelatedField(
                        view_name='bookmark-detail'),
                    Note: serializers.HyperlinkedRelatedField(
                        view_name='note-detail'),
                },
                source='tagged_item',
                read_only=False,
            )

            class Meta:
                model = Tag
                exclude = ('id', 'content_type', 'object_id', )

        serializer = TagSerializer(data={
            'tag': 'reminder',
            'tagged_item': reverse('note-detail', kwargs={'pk': self.note.pk})
        }, context={'request': request})
        serializer.is_valid()
        expected = {
            'tagged_item': 'http://testserver/note/1/',
            'tag': 'reminder'
        }
        self.assertEqual(serializer.data, expected)

    def test_configuration_error(self):
        class TagSerializer(serializers.ModelSerializer):
            tagged_item = GenericRelatedField(
                {
                    Bookmark: BookmarkSerializer(),
                    Note: serializers.HyperlinkedRelatedField(
                        view_name='note-detail'),
                },
                source='tagged_item',
                read_only=False,
            )

            class Meta:
                model = Tag
                exclude = ('id', 'content_type', 'object_id', )

        serializer = TagSerializer(data={
            'tag': 'reminder',
            'tagged_item': 'just a string'
        })

        with self.assertRaises(ImproperlyConfigured):
            tagged_item = serializer.fields['tagged_item']
            tagged_item.determine_serializer_for_data('just a string')

    def test_not_registered_view_name(self):
        class TagSerializer(serializers.ModelSerializer):
            tagged_item = GenericRelatedField(
                {
                    Bookmark: serializers.HyperlinkedRelatedField(
                        view_name='bookmark-detail'),
                },
                source='tagged_item',
                read_only=False,
            )

            class Meta:
                model = Tag
                exclude = ('id', 'content_type', 'object_id', )

        serializer = TagSerializer(data={
            'tag': 'reminder',
            'tagged_item': reverse('note-detail', kwargs={'pk': self.note.pk})
        })
        self.assertFalse(serializer.is_valid())

    def test_invalid_url(self):
        class TagSerializer(serializers.ModelSerializer):
            tagged_item = GenericRelatedField(
                {
                    Bookmark: serializers.HyperlinkedRelatedField(
                        view_name='bookmark-detail'),
                },
                source='tagged_item',
                read_only=False,
            )

            class Meta:
                model = Tag
                exclude = ('id', 'content_type', 'object_id', )

        serializer = TagSerializer(data={
            'tag': 'reminder',
            'tagged_item': 'foo-bar'
        })

        message = 'Could not determine a valid serializer for value %r.'
        expected = {'tagged_item': [message % 'foo-bar']}

        self.assertFalse(serializer.is_valid())
        self.assertEqual(expected, serializer.errors)

    def test_serializer_save(self):
        class TagSerializer(serializers.ModelSerializer):
            tagged_item = GenericRelatedField(
                {
                    Bookmark: serializers.HyperlinkedRelatedField(
                        view_name='bookmark-detail'),
                    Note: serializers.HyperlinkedRelatedField(
                        view_name='note-detail'),
                },
                source='tagged_item',
                read_only=False,
            )

            class Meta:
                model = Tag
                exclude = ('id', 'content_type', 'object_id', )

        serializer = TagSerializer(data={
            'tag': 'reminder',
            'tagged_item': reverse('note-detail', kwargs={'pk': self.note.pk})
        })
        serializer.is_valid()
        serializer.save()
        tag = Tag.objects.get(pk=3)
        self.assertEqual(tag.tagged_item, self.note)

    def test_nullable_relation_serializer_save(self):
        class DetachableSerializer(serializers.ModelSerializer):
            content_object = GenericRelatedField(
                {
                    Bookmark: serializers.HyperlinkedRelatedField(
                        view_name='bookmark-detail'),
                    Note: serializers.HyperlinkedRelatedField(
                        view_name='note-detail'),
                },
                source='content_object',
                read_only=False,
                required=False
            )

            class Meta:
                model = Detachable
                exclude = ('id', 'content_type', 'object_id', )

        serializer = DetachableSerializer(data={'name': 'foo'})
        serializer.is_valid()
        serializer.save()
        freeagent = Detachable.objects.get(pk=1)
        self.assertEqual(freeagent.name, 'foo')
        self.assertEqual(freeagent.content_object, None)
