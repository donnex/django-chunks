# -*- coding: utf-8 -*-
from django import template
from django.db import models
from django.core.cache import cache

register = template.Library()

Chunk = models.get_model('chunks', 'chunk')


def do_chunk(parser, token):
    # split_contents() knows not to split quoted strings.
    tokens = token.split_contents()
    if len(tokens) < 2 or len(tokens) > 3:
        raise template.TemplateSyntaxError, "%r tag should have either 2 or 3 arguments" % (tokens[0],)
    if len(tokens) == 2:
        tag_name, key = tokens
        cache_time = None
    if len(tokens) == 3:
        tag_name, key, cache_time = tokens
        cache_time = int(cache_time)
    key = ensure_quoted_string(key, "%r tag's argument should be in quotes" % tag_name)
    return ChunkNode(key, cache_time)


class ChunkNode(template.Node):
    def __init__(self, key, cache_time=None):
        self.key = key
        self.cache_time = cache_time

    def render(self, context):
        try:
            # Try to fetch cached node
            cache_key = Chunk.get_cache_key(self.key)
            chunk = cache.get(cache_key)

            if chunk is None:
                chunk = Chunk.objects.get(key=self.key)

                # Cache node
                cache.set(cache_key, chunk, self.cache_time)
            content = u'<div class="chunk" id="{}">{}</div>'.format(
                chunk.key, chunk.content)
        except Chunk.DoesNotExist:
            content = ''
        return content


def do_get_chunk(parser, token):
    tokens = token.split_contents()
    if len(tokens) != 4 or tokens[2] != 'as':
        raise template.TemplateSyntaxError, 'Invalid syntax. Usage: {%% %s "key" as varname %%}' % tokens[0]
    tagname, key, varname = tokens[0], tokens[1], tokens[3]
    key = ensure_quoted_string(key, "Key argument to %r must be in quotes" % tagname)
    return GetChunkNode(key, varname)


class GetChunkNode(template.Node):
    def __init__(self, key, varname):
        self.key = key
        self.varname = varname

    def render(self, context):
        try:
            chunk = Chunk.objects.get(key=self.key)
        except Chunk.DoesNotExist:
            chunk = None
        context[self.varname] = chunk
        return ''


def ensure_quoted_string(string, error_message):
    '''
    Check to see if the key is properly double/single quoted and
    returns the string without quotes
    '''
    if not (string[0] == string[-1] and string[0] in ('"', "'")):
        raise template.TemplateSyntaxError, error_message
    return string[1:-1]


register.tag('chunk', do_chunk)
register.tag('get_chunk', do_get_chunk)
