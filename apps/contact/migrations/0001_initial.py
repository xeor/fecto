# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Location'
        db.create_table('contact_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(db_index=True, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.TextField')(db_index=True, null=True, blank=True)),
        ))
        db.send_create_signal('contact', ['Location'])


    def backwards(self, orm):
        
        # Deleting model 'Location'
        db.delete_table('contact_location')


    models = {
        'contact.location': {
            'Meta': {'ordering': "['name']", 'object_name': 'Location'},
            'address': ('django.db.models.fields.TextField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'})
        }
    }

    complete_apps = ['contact']
