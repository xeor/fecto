# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Site.value'
        db.add_column('siteconfig_site', 'value', self.gf('django.db.models.fields.TextField')(default=''), keep_default=False)

        # Adding unique constraint on 'Site', fields ['name']
        db.create_unique('siteconfig_site', ['name'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Site', fields ['name']
        db.delete_unique('siteconfig_site', ['name'])

        # Deleting field 'Site.value'
        db.delete_column('siteconfig_site', 'value')


    models = {
        'siteconfig.site': {
            'Meta': {'object_name': 'Site'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'default': "''"})
        }
    }

    complete_apps = ['siteconfig']
