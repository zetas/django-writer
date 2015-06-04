# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'StripeEvent'
        db.create_table(u'account_stripeevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stripe_event_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=150)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('recorded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('event_type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stripe_events', to=orm['account.WUser'])),
        ))
        db.send_create_signal(u'account', ['StripeEvent'])


    def backwards(self, orm):
        # Deleting model 'StripeEvent'
        db.delete_table(u'account_stripeevent')


    models = {
        u'account.license': {
            'Meta': {'object_name': 'License'},
            'assigned_user': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'license'", 'unique': 'True', 'null': 'True', 'to': u"orm['account.WUser']"}),
            'creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'purchasing_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'purchased_license'", 'to': u"orm['account.WUser']"}),
            'redemption_code': ('django.db.models.fields.CharField', [], {'default': "'SQLVHV-K431GV-ZW4Q8G-HHP2MS'", 'unique': 'True', 'max_length': '255'}),
            'sent_to': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'term_in_days': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'account.stripeevent': {
            'Meta': {'ordering': "['-recorded']", 'object_name': 'StripeEvent'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'event_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recorded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'stripe_event_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stripe_events'", 'to': u"orm['account.WUser']"})
        },
        u'account.wuser': {
            'Meta': {'object_name': 'WUser'},
            'account_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'cc_last_4': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'cc_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
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
            'stripe_customer_id': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'stripe_subscription_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'zip': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['account']