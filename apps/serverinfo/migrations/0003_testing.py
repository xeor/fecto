# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Municipality'
        db.delete_table('serverinfo_municipality')

        # Deleting model 'County'
        db.delete_table('serverinfo_county')

        # Deleting model 'Location'
        db.delete_table('serverinfo_location')

        # Adding model 'CompanyContactPerson'
        db.create_table('serverinfo_companycontactperson', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['serverinfo.Company'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal('serverinfo', ['CompanyContactPerson'])

        # Adding model 'Case'
        db.create_table('serverinfo_case', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['serverinfo.Client'])),
            ('company_contact_person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['serverinfo.CompanyContactPerson'])),
        ))
        db.send_create_signal('serverinfo', ['Case'])

        # Adding model 'Company'
        db.create_table('serverinfo_company', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
        ))
        db.send_create_signal('serverinfo', ['Company'])

        # Adding model 'Client'
        db.create_table('serverinfo_client', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['serverinfo.Company'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
        ))
        db.send_create_signal('serverinfo', ['Client'])


    def backwards(self, orm):
        
        # Adding model 'Municipality'
        db.create_table('serverinfo_municipality', (
            ('county', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['serverinfo.County'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('serverinfo', ['Municipality'])

        # Adding model 'County'
        db.create_table('serverinfo_county', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True)),
        ))
        db.send_create_signal('serverinfo', ['County'])

        # Adding model 'Location'
        db.create_table('serverinfo_location', (
            ('county', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['serverinfo.County'])),
            ('municipality', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['serverinfo.Municipality'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('serverinfo', ['Location'])

        # Deleting model 'CompanyContactPerson'
        db.delete_table('serverinfo_companycontactperson')

        # Deleting model 'Case'
        db.delete_table('serverinfo_case')

        # Deleting model 'Company'
        db.delete_table('serverinfo_company')

        # Deleting model 'Client'
        db.delete_table('serverinfo_client')


    models = {
        'contact.location': {
            'Meta': {'ordering': "['name']", 'object_name': 'Location'},
            'address': ('django.db.models.fields.TextField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'})
        },
        'serverinfo.case': {
            'Meta': {'object_name': 'Case'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['serverinfo.Client']"}),
            'company_contact_person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['serverinfo.CompanyContactPerson']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'serverinfo.client': {
            'Meta': {'object_name': 'Client'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['serverinfo.Company']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'serverinfo.company': {
            'Meta': {'object_name': 'Company'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'serverinfo.companycontactperson': {
            'Meta': {'object_name': 'CompanyContactPerson'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['serverinfo.Company']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
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
