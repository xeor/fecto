# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Text.app'
        db.add_column('siteconfig_text', 'app', self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=255, db_index=True), keep_default=False)

        # Adding field 'Text.default'
        db.add_column('siteconfig_text', 'default', self.gf('django.db.models.fields.TextField')(default=''), keep_default=False)

        # Adding field 'Text.permission'
        db.add_column('siteconfig_text', 'permission', self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=255, db_index=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Text.app'
        db.delete_column('siteconfig_text', 'app')

        # Deleting field 'Text.default'
        db.delete_column('siteconfig_text', 'default')

        # Deleting field 'Text.permission'
        db.delete_column('siteconfig_text', 'permission')


    models = {
        'siteconfig.site': {
            'Meta': {'object_name': 'Site'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'default': "''"})
        },
        'siteconfig.text': {
            'Meta': {'object_name': 'Text'},
            'app': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'default': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'permission': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'default': "''"})
        }
    }

    complete_apps = ['siteconfig']
