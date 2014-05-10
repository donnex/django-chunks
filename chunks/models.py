# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.core.cache import cache


from ckeditor.fields import RichTextField


class Chunk(models.Model):
    """
    A Chunk is a piece of content associated
    with a unique key that can be inserted into
    any template with the use of a special template
    tag
    """

    CACHE_PREFIX = 'chunk:'

    name = models.CharField(
        _(u'Name'),
        max_length=100)

    key = models.CharField(
        _(u'Key'),
        help_text=_(u'A unique name for this chunk of content'),
        blank=False,
        max_length=255,
        unique=True)

    content = RichTextField(
        _(u'Content'),
        blank=True)

    description = models.CharField(
        _(u'Description'),
        blank=True,
        max_length=64,
        help_text=_(u'Short description'))

    class Meta:
        verbose_name = _(u'chunk')
        verbose_name_plural = _(u'chunks')

    def __unicode__(self):
        return self.key

    def set_node_cache(self, cache_time):
        cache_key = Chunk.CACHE_PREFIX + self.key
        cache.set(cache_key, self, cache_time)

    @staticmethod
    def get_cached_node(key):
        cache_key = Chunk.CACHE_PREFIX + key
        chunk = cache.get(cache_key)

        return chunk


@receiver(post_save, sender=Chunk)
def _chunk_post_save(sender, instance, **kwargs):
    """Invalidate the cache after chunk save"""

    cache_key = Chunk.CACHE_PREFIX + instance.key
    cache.delete(cache_key)
