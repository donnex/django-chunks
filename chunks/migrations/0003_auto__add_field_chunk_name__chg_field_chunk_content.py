# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Chunk.name'
        db.add_column(u'chunks_chunk', 'name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)


        # Changing field 'Chunk.content'
        db.alter_column(u'chunks_chunk', 'content', self.gf('ckeditor.fields.RichTextField')())

    def backwards(self, orm):
        # Deleting field 'Chunk.name'
        db.delete_column(u'chunks_chunk', 'name')


        # Changing field 'Chunk.content'
        db.alter_column(u'chunks_chunk', 'content', self.gf('django.db.models.fields.TextField')())

    models = {
        u'chunks.chunk': {
            'Meta': {'object_name': 'Chunk'},
            'content': ('ckeditor.fields.RichTextField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['chunks']