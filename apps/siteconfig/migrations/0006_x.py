# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Removing unique constraint on 'Text', fields ['name']
        db.delete_unique('siteconfig_text', ['name'])

        # Removing unique constraint on 'Text', fields ['app']
        db.delete_unique('siteconfig_text', ['app'])

        # Removing unique constraint on 'Text', fields ['permission']
        db.delete_unique('siteconfig_text', ['permission'])

        # Adding index on 'Text', fields ['value']
        db.create_index('siteconfig_text', ['value'])


    def backwards(self, orm):
        
        # Removing index on 'Text', fields ['value']
        db.delete_index('siteconfig_text', ['value'])

        # Adding unique constraint on 'Text', fields ['permission']
        db.create_unique('siteconfig_text', ['permission'])

        # Adding unique constraint on 'Text', fields ['app']
        db.create_unique('siteconfig_text', ['app'])

        # Adding unique constraint on 'Text', fields ['name']
        db.create_unique('siteconfig_text', ['name'])


    models = {
        'siteconfig.site': {
            'Meta': {'object_name': 'Site'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'default': "''"})
        },
        'siteconfig.text': {
            'Meta': {'object_name': 'Text'},
            'app': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'db_index': 'True'}),
            'default': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'permission': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'db_index': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'default': "''", 'db_index': 'True'})
        }
    }

    complete_apps = ['siteconfig']
