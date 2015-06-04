# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'PaperSubmission.slug'
        db.alter_column(u'papers_papersubmission', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=100))

    def backwards(self, orm):

        # Changing field 'PaperSubmission.slug'
        db.alter_column(u'papers_papersubmission', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=100))

    models = {
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
        },
        u'papers.analyzationresult': {
            'Meta': {'object_name': 'AnalyzationResult'},
            'average_syllables_per_word': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'average_words_per_sentence': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'character_count': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paper': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['papers.Paper']"}),
            'percent_words_gt3_syllables': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'sentence_count': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'text_length': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'total_syllables': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'word_count': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'word_occurrence': ('django.db.models.fields.TextField', [], {}),
            'words_gt3_syllables': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'papers.paper': {
            'Meta': {'object_name': 'Paper'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.WUser']"})
        },
        u'papers.papersubmission': {
            'Meta': {'object_name': 'PaperSubmission'},
            'date_submitted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paper': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['papers.Paper']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '300'}),
            'submitted_to': ('django.db.models.fields.EmailField', [], {'max_length': '75'})
        }
    }

    complete_apps = ['papers']