# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Paper'
        db.create_table(u'papers_paper', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.WUser'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'papers', ['Paper'])

        # Adding model 'PaperSubmission'
        db.create_table(u'papers_papersubmission', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('paper', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['papers.Paper'])),
            ('pdf_link', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('submitted_to', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('date_submitted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'papers', ['PaperSubmission'])

        # Adding model 'AnalyzationResult'
        db.create_table(u'papers_analyzationresult', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('paper', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['papers.Paper'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('sentence_count', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('word_count', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('average_words_per_sentence', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('total_syllables', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('average_syllables_per_word', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('words_gt3_syllables', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('percent_words_gt3_syllables', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('text_length', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('character_count', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('word_occurrence', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'papers', ['AnalyzationResult'])


    def backwards(self, orm):
        # Deleting model 'Paper'
        db.delete_table(u'papers_paper')

        # Deleting model 'PaperSubmission'
        db.delete_table(u'papers_papersubmission')

        # Deleting model 'AnalyzationResult'
        db.delete_table(u'papers_analyzationresult')


    models = {
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
            'pdf_link': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'submitted_to': ('django.db.models.fields.EmailField', [], {'max_length': '75'})
        }
    }

    complete_apps = ['papers']