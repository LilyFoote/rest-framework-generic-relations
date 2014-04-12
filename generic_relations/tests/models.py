from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericRelation, GenericForeignKey
from django.db import models


class Tag(models.Model):
    """
    Tags have a descriptive slug, and are attached to an arbitrary object.
    """
    tag = models.SlugField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    tagged_item = GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return self.tag


class Bookmark(models.Model):
    """
    A URL bookmark that may have multiple tags attached.
    """
    url = models.URLField()
    tags = GenericRelation(Tag)

    def __unicode__(self):
        return 'Bookmark: %s' % self.url


class Note(models.Model):
    """
    A textual note that may have multiple tags attached.
    """
    text = models.TextField()
    tags = GenericRelation(Tag)

    def __unicode__(self):
        return 'Note: %s' % self.text


class Contact(models.Model):
    """
    A textual note that may have multiple tags attached.
    """
    name = models.TextField()
    slug = models.SlugField()
    tags = GenericRelation(Tag)

    def __unicode__(self):
        return 'Contact: %s' % self.name
