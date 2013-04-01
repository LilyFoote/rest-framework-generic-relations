# Rest Framework Generic Relations

# API Reference

If you want to serialize a generic foreign key, you need to define a `GenericRelatedField` with a configuration dictionary as first argument, that describes the representation of each model you possibly want to connect to the generic foreign key.

For example, given the following model for a tag, which has a generic relationship with other arbitrary models:

    class TaggedItem(models.Model):
        """
        Tags arbitrary model instances using a generic relation.

        See: https://docs.djangoproject.com/en/dev/ref/contrib/contenttypes/
        """
        tag_name = models.SlugField()
        content_type = models.ForeignKey(ContentType)
        object_id = models.PositiveIntegerField()
        tagged_object = GenericForeignKey('content_type', 'object_id')

        def __unicode__(self):
            return self.tag

And the following two models, which may be have associated tags:

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

Now we define serializers for each model that may get associated with tags.

    class BookmarkSerializer(serializers.ModelSerializer):
        """
        A simple `ModelSerializer` subclass for serializing `Bookmark` objects.
        """
        class Meta:
            model = Bookmark
            exclude = ('id', )


    class NoteSerializer(serializers.ModelSerializer):
        """
        A simple `ModelSerializer` subclass for serializing `Note` objects.
        """
        class Meta:
            model = Note
            exclude = ('id', )

The model serializer for the `Tag` model could look like this:

    from generic_relations.relations import GenericRelatedField


    class TagSerializer(serializers.ModelSerializer):
        """
        A `Tag` serializer with a `GenericRelatedField` mapping all possible
        models to their respective serializers.
        """
        tagged_object = GenericRelatedField({
            Bookmark: BookmarkSerializer(),
            Note: NoteSerializer()
        }, read_only=True)

        class Meta:
            model = Tag
            exclude = ('id', )

The JSON representation of a `Tag` object with `name='django'` and its generic foreign key pointing at a `Bookmark` object with `url='https://www.djangoproject.com/'` would look like this:

    {
        'tagged_object': {
            'url': 'https://www.djangoproject.com/'
        },
        'tag_name': 'django'
    }

If you want to have your generic foreign key represented as hyperlink, simply use `HyperlinkedRelatedField` objects:

    class TagSerializer(serializers.ModelSerializer):
        """
        A `Tag` serializer with a `GenericRelatedField` mapping all possible
        models to properly set up `HyperlinkedRelatedField`s.
        """
        tagged_object = serializers.GenericRelatedField({
            Bookmark: serializers.HyperlinkedRelatedField(view_name='bookmark-detail'),
            Note: serializers.HyperlinkedRelatedField(view_name='note-detail'),
        }, read_only=True)

        class Meta:
            model = Tag
            exclude = ('id', )

The JSON representation of the same `Tag` example object could now look something like this:

    {
        'tagged_object': '/bookmark/1/',
        'tag_name': 'django'
    }

These examples cover the default behavior of generic foreign key representation. However, you may also want to write to generic foreign key fields through your API.

By default, the `GenericRelatedField` can be used with `read_only=False` only if you use `HyperlinkedRelatedField` as representation for every model you register with your `GenericRelatedField`.

This `Tag` serializer is able to write to it's generic foreign key field:

    class TagSerializer(serializers.ModelSerializer):
            """
            A `Tag` serializer with a `GenericRelatedField` mapping all possible
            models to properly set up `HyperlinkedRelatedField`s.
            """
            tagged_object = GenericRelatedField({
                Bookmark: serializers.HyperlinkedRelatedField(view_name='bookmark-detail'),
                Note: serializers.HyperlinkedRelatedField(view_name='note-detail'),
            }, read_only=False)

            class Meta:
                model = Tag
                exclude = ('id', )

The following operations would create a `Tag` object with it's `tagged_object` property pointing at the `Bookmark` object found at the given detail end point.

    tag_serializer = TagSerializer(data={
        'tag_name': 'python'
        'tagged_object': '/bookmark/1/'
    })

    tag_serializer.is_valid()
    tag_serializer.save()

If you feel that this default behavior doesn't suit your needs, you can subclass `GenericRelatedField` and override its `determine_serializer_for_data` method to implement your own way of decision-making.

A few things you should note:

* Although `GenericForeignKey` fields can be set to any model object, the `GenericRelatedField` only handles models explicitly defined in its configuration dictionary.
* Reverse generic keys, expressed using the `GenericRelation` field, can be serialized using the regular relational field types, since the type of the target in the relationship is always known.
* You can mix `ModelSerializer` and `HyperlinkedRelatedField` in one `GenericRelatedField` configuration dictionary for deserialization purposes. It is considered bad practice though.
* If you mix `ModelSerializer` and `HyperlinkedRelatedField` in one `GenericRelatedField` configuration dictionary, the serialization process (PUT/POST) will raise a `ConfigurationError`.

For more information see [the Django documentation on generic relations][generic-relations].
