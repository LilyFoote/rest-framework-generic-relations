Quickstart
==========

We'll assume you have two simple models and a third model with a :class:`~django:django.contrib.contenttypes.fields.GenericForeignKey`::

    class TaggedItem(models.Model):
        tag_name = models.SlugField()
        content_type = models.ForeignKey(ContentType)
        object_id = models.PositiveIntegerField()
        tagged_object = GenericForeignKey('content_type', 'object_id')


    class Bookmark(models.Model):
        """A bookmark consists of a URL, and 0 or more descriptive tags."""
        url = models.URLField()
        tags = GenericRelation(TaggedItem)


    class Note(models.Model):
        """A note consists of some text, and 0 or more descriptive tags."""
        text = models.CharField(max_length=1000)
        tags = GenericRelation(TaggedItem)


You can serialize a ``TaggedItem`` by defining a ``Serializer`` with a ``GenericRelatedField``::

    class TagSerializer(serializers.ModelSerializer):
        """
        A Tag serializer with a GenericRelatedField mapping all
        possible models to HyperlinkedRelatedFields.
        """
        tagged_object = serializers.GenericRelatedField({
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

The JSON representation of a ``TaggedItem`` will now look something like this::

    {
        "tagged_object": "/bookmark/1/",
        "tag_name": "django"
    }
