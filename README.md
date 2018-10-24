# Rest Framework Generic Relations [![Build Status](https://travis-ci.org/Ian-Foote/rest-framework-generic-relations.svg?branch=pep8)](https://travis-ci.org/Ian-Foote/rest-framework-generic-relations)

This library implements [Django REST Framework](http://www.django-rest-framework.org/) serializers to handle generic foreign keys.

# Installation

Install using `pip`...

    pip install  rest-framework-generic-relations

Add `'generic_relations'` to your `INSTALLED_APPS` setting.

    INSTALLED_APPS = (
        ...
        'generic_relations',
    )



# API Reference

## GenericRelatedField

This field serializes generic foreign keys. For a primer on generic foreign keys, first see: https://docs.djangoproject.com/en/dev/ref/contrib/contenttypes/


Let's assume a `TaggedItem` model which has a generic relationship with other arbitrary models:

```python
class TaggedItem(models.Model):
    tag_name = models.SlugField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    tagged_object = GenericForeignKey('content_type', 'object_id')
```

And the following two models, which may have associated tags:

```python
class Bookmark(models.Model):
    """
    A bookmark consists of a URL, and 0 or more descriptive tags.
    """
    url = models.URLField()
    tags = GenericRelation(TaggedItem)

class Note(models.Model):
    """
    A note consists of some text, and 0 or more descriptive tags.
    """
    text = models.CharField(max_length=1000)
    tags = GenericRelation(TaggedItem)
```

Now we define serializers for each model that may get associated with tags.

```python
class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ('url',)

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('text',)
```

The model serializer for the `TaggedItem` model could look like this:

```python
from generic_relations.relations import GenericRelatedField

class TagSerializer(serializers.ModelSerializer):
    """
    A `TaggedItem` serializer with a `GenericRelatedField` mapping all possible
    models to their respective serializers.
    """
    tagged_object = GenericRelatedField({
        Bookmark: BookmarkSerializer(),
        Note: NoteSerializer()
    })

    class Meta:
        model = TaggedItem
        fields = ('tag_name', 'tagged_object')
```

The JSON representation of a `TaggedItem` object with `name='django'` and its generic foreign key pointing at a `Bookmark` object with `url='https://www.djangoproject.com/'` would look like this:

```json
{
    "tagged_object": {
        "url": "https://www.djangoproject.com/"
    },
    "tag_name": "django"
}
```

If you want to have your generic foreign key represented as hyperlink, simply use `HyperlinkedRelatedField` objects:

```python
class TagSerializer(serializers.ModelSerializer):
    """
    A `Tag` serializer with a `GenericRelatedField` mapping all possible
    models to properly set up `HyperlinkedRelatedField`s.
    """
    tagged_object = GenericRelatedField({
        Bookmark: serializers.HyperlinkedRelatedField(
            queryset = Bookmark.objects.all(),
            view_name='bookmark-detail',
        ),
        Note: serializers.HyperlinkedRelatedField(
            queryset = Note.objects.all(),
            view_name='note-detail',
        ),
    })

    class Meta:
        model = TaggedItem
        fields = ('tag_name', 'tagged_object')
```

The JSON representation of the same `TaggedItem` example object could now look something like this:

```json
{
    "tagged_object": "/bookmark/1/",
    "tag_name": "django"
}
```

## Writing to generic foreign keys

The above `TagSerializer` is also writable. By default, a `GenericRelatedField` iterates over its nested serializers and returns the value of the first serializer that is actually able to perform `to_internal_value()` without any errors.
Note, that (at the moment) only `HyperlinkedRelatedField` is able to serialize model objects out of the box.


The following operations would create a `TaggedItem` object with it's `tagged_object` property pointing at the `Bookmark` object found at the given detail end point.

```python
tag_serializer = TagSerializer(data={
    'tag_name': 'python'
    'tagged_object': '/bookmark/1/'
})

tag_serializer.is_valid()
tag_serializer.save()
```

If you feel that this default behavior doesn't suit your needs, you can subclass `GenericRelatedField` and override its `get_serializer_for_instance` or `get_deserializer_for_data` respectively to implement your own way of decision-making.

## GenericModelSerializer

Sometimes you may want to serialize a single list of different top-level things. For instance, suppose I have an API view that returns what items are on my bookshelf. Let's define some models:

```python
from django.core.validators import MaxValueValidator

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)

class Bluray(models.Model):
    title = models.CharField(max_length=255)
    rating = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(5)],
    )
```

Then we could have a serializer for each type of object:

```python
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'author')

class BluraySerializer(serializers.ModelSerializer):
    class Meta:
        model = Bluray
        fields = ('title', 'rating')
```

Now we can create a generic list serializer, which delegates to the above serializers based on the type of model it's serializing:

```python
bookshelf_item_serializer = GenericModelSerializer(
    {
        Book: BookSerializer(),
        Bluray: BluraySerializer(),
    },
    many=True,
)
```

Then we can serialize a mixed list of items:

```python
>>> bookshelf_item_serializer.to_representation([
    Book.objects.get(title='War and Peace'),
    Bluray.objects.get(title='Die Hard'),
    Bluray.objects.get(title='Shawshank Redemption'),
    Book.objects.get(title='To Kill a Mockingbird'),
])

[
    {'title': 'War and Peace', 'author': 'Leo Tolstoy'},
    {'title': 'Die Hard', 'rating': 5},
    {'title': 'Shawshank Redemption', 'rating': 5},
    {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee'}
]
```


## A few things you should note:

* Although `GenericForeignKey` fields can be set to any model object, the `GenericRelatedField` only handles models explicitly defined in its configuration dictionary.
* Reverse generic keys, expressed using the `GenericRelation` field, can be serialized using the regular relational field types, since the type of the target in the relationship is always known.
* The order in which you register serializers matters as far as write operations are concerned.
* Unless you provide a custom `get_deserializer_for_data()` method, only `HyperlinkedRelatedField` provides write access to generic model relations.
