# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ckeditor.fields import RichTextField


class Chunk(models.Model):
    """
    A Chunk is a piece of content associated
    with a unique key that can be inserted into
    any template with the use of a special template
    tag
    """

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

