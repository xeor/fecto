# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding M2M table for field testmtom on 'Misc'
        db.create_table('serverinfo_misc_testmtom', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('misc', models.ForeignKey(orm['serverinfo.misc'], null=False)),
            ('misctype', models.ForeignKey(orm['serverinfo.misctype'], null=False))
        ))
        db.create_unique('serverinfo_misc_testmtom', ['misc_id', 'misctype_id'])


    def backwards(self, orm):
        
        # Removing M2M table for field testmtom on 'Misc'
        db.delete_table('serverinfo_misc_testmtom')


    models = {
        'contact.location': {
            'Meta': {'ordering': "['name']", 'object_name': 'Location'},
            'address': ('django.db.models.fields.TextField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'})
        },
        'serverinfo.ip': {
            'Meta': {'ordering': "['vlan', 'ip']", 'object_name': 'IP'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'unique': 'True', 'max_length': '15'}),
            'vlan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['serverinfo.Vlan']", 'null': 'True', 'blank': 'True'})
        },
        'serverinfo.misc': {
            'Meta': {'ordering': "['name']", 'object_name': 'Misc'},
            'description': ('django.db.models.fields.TextField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contact.Location']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['serverinfo.MiscType']"}),
            'testmtom': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'testing'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['serverinfo.MiscType']"}),
            'url': ('django.db.models.fields.URLField', [], {'db_index': 'True', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'serverinfo.miscfieldtype': {
            'Meta': {'object_name': 'MiscFieldType'},
            'description': ('django.db.models.fields.TextField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'})
        },
        'serverinfo.misctype': {
            'Meta': {'object_name': 'MiscType'},
            'autopopulated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'fieldType': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['serverinfo.MiscFieldType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'multiple_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'})
        },
        'serverinfo.server': {
            'Meta': {'ordering': "['name']", 'object_name': 'Server'},
            'attributes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['serverinfo.Misc']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'function': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['serverinfo.IP']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'db_index': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'reg_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': '2', 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'upd_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'virtual': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'serverinfo.vlan': {
            'Meta': {'ordering': "['name']", 'object_name': 'Vlan'},
            'description': ('django.db.models.fields.TextField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contact.Location']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'}),
            'network': ('django.db.models.fields.CharField', [], {'max_length': '18', 'db_index': 'True'}),
            'skipEnd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'skipFirst': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vlanID': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['serverinfo']
