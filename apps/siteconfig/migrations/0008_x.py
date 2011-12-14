# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Text.varType'
        db.alter_column('siteconfig_text', 'varType', self.gf('django.db.models.fields.CharField')(max_length=64))


    def backwards(self, orm):
        
        # Changing field 'Text.varType'
        db.alter_column('siteconfig_text', 'varType', self.gf('django.db.models.fields.TextField')())


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
            'permission': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'varType': ('django.db.models.fields.CharField', [], {'default': "'text'", 'max_length': '64'})
        }
    }

    complete_apps = ['siteconfig']
