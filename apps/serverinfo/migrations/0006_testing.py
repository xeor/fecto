# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Case'
        db.delete_table('serverinfo_case')

        # Deleting model 'manyCase'
        db.delete_table('serverinfo_manycase')

        # Deleting model 'CompanyContactPerson'
        db.delete_table('serverinfo_companycontactperson')

        # Deleting model 'Company'
        db.delete_table('serverinfo_company')

        # Deleting model 'Client'
        db.delete_table('serverinfo_client')


    def backwards(self, orm):
        
        # Adding model 'Case'
        db.create_table('serverinfo_case', (
            ('otherCase', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['serverinfo.manyCase'])),
            ('company_contact_person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['serverinfo.CompanyContactPerson'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['serverinfo.Client'])),
        ))
        db.send_create_signal('serverinfo', ['Case'])

        # Adding model 'manyCase'
        db.create_table('serverinfo_manycase', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
        ))
        db.send_create_signal('serverinfo', ['manyCase'])

        # Adding model 'CompanyContactPerson'
        db.create_table('serverinfo_companycontactperson', (
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['serverinfo.Company'])),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('serverinfo', ['CompanyContactPerson'])

        # Adding model 'Company'
        db.create_table('serverinfo_company', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
        ))
        db.send_create_signal('serverinfo', ['Company'])

        # Adding model 'Client'
        db.create_table('serverinfo_client', (
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['serverinfo.Company'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
        ))
        db.send_create_signal('serverinfo', ['Client'])


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
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['serverinfo.Server']", 'null': 'True', 'blank': 'True'}),
            'vlan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['serverinfo.Vlan']", 'null': 'True', 'blank': 'True'})
        },
        'serverinfo.misc': {
            'Meta': {'ordering': "['infoType', 'name']", 'object_name': 'Misc'},
            'description': ('django.db.models.fields.TextField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'infoType': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['serverinfo.MiscTypes']"}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contact.Location']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'db_index': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'serverinfo.misctypes': {
            'Meta': {'object_name': 'MiscTypes'},
            'autopopulated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'})
        },
        'serverinfo.server': {
            'Meta': {'ordering': "['name']", 'object_name': 'Server'},
            'autogenerated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'function': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
