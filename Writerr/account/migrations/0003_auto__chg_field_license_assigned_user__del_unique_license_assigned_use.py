# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'License', fields ['assigned_user']
        db.delete_unique(u'account_license', ['assigned_user_id'])


        # Changing field 'License.assigned_user'
        db.alter_column(u'account_license', 'assigned_user_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['account.WUser']))

    def backwards(self, orm):

        # Changing field 'License.assigned_user'
        db.alter_column(u'account_license', 'assigned_user_id', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, null=True, to=orm['account.WUser']))
        # Adding unique constraint on 'License', fields ['assigned_user']
        db.create_unique(u'account_license', ['assigned_user_id'])


    models = {
        u'account.license': {
            'Meta': {'object_name': 'License'},
            'assigned_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'license'", 'null': 'True', 'to': u"orm['account.WUser']"}),
            'creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'purchasing_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'purchased_license'", 'to': u"orm['account.WUser']"}),
            'redemption_code': ('django.db.models.fields.CharField', [], {'default': "'RAOFGQ-QGJSHE-IXZWN7-NP4NO1'", 'unique': 'True', 'max_length': '255'}),
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