# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WUser'
        db.create_table(u'account_wuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=255, db_index=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('zip', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=5, null=True, blank=True)),
            ('account_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'account', ['WUser'])

        # Adding model 'License'
        db.create_table(u'account_license', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('purchasing_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='purchased_license', to=orm['account.WUser'])),
            ('assigned_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='license', null=True, to=orm['account.WUser'])),
            ('creation', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('term_in_days', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('redemption_code', self.gf('django.db.models.fields.CharField')(default='PJOBTX-551QLX-BGGA8B-LY8YJ3', unique=True, max_length=255)),
        ))
        db.send_create_signal(u'account', ['License'])


    def backwards(self, orm):
        # Deleting model 'WUser'
        db.delete_table(u'account_wuser')

        # Deleting model 'License'
        db.delete_table(u'account_license')


    models = {
        u'account.license': {
            'Meta': {'object_name': 'License'},
            'assigned_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'license'", 'null': 'True', 'to': u"orm['account.WUser']"}),
            'creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'purchasing_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'purchased_license'", 'to': u"orm['account.WUser']"}),
            'redemption_code': ('django.db.models.fields.CharField', [], {'default': "'XUP733-5PTSGX-UKZ5IN-6UM91D'", 'unique': 'True', 'max_length': '255'}),
            'term_in_days': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'account.wuser': {
            'Meta': {'object_name': 'WUser'},
            'account_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'zip': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['account']