# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PaperComment'
        db.create_table(u'papers_papercomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('paper', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['papers.Paper'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.WUser'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'papers', ['PaperComment'])

        # Deleting field 'AnalyzationResult.average_syllables_per_word'
        db.delete_column(u'papers_analyzationresult', 'average_syllables_per_word')

        # Deleting field 'AnalyzationResult.text_length'
        db.delete_column(u'papers_analyzationresult', 'text_length')

        # Deleting field 'AnalyzationResult.word_count'
        db.delete_column(u'papers_analyzationresult', 'word_count')

        # Deleting field 'AnalyzationResult.total_syllables'
        db.delete_column(u'papers_analyzationresult', 'total_syllables')

        # Deleting field 'AnalyzationResult.date_created'
        db.delete_column(u'papers_analyzationresult', 'date_created')

        # Deleting field 'AnalyzationResult.percent_words_gt3_syllables'
        db.delete_column(u'papers_analyzationresult', 'percent_words_gt3_syllables')

        # Deleting field 'AnalyzationResult.average_words_per_sentence'
        db.delete_column(u'papers_analyzationresult', 'average_words_per_sentence')

        # Deleting field 'AnalyzationResult.words_gt3_syllables'
        db.delete_column(u'papers_analyzationresult', 'words_gt3_syllables')

        # Deleting field 'AnalyzationResult.word_occurrence'
        db.delete_column(u'papers_analyzationresult', 'word_occurrence')

        # Deleting field 'AnalyzationResult.sentence_count'
        db.delete_column(u'papers_analyzationresult', 'sentence_count')

        # Deleting field 'AnalyzationResult.character_count'
        db.delete_column(u'papers_analyzationresult', 'character_count')

        # Adding field 'AnalyzationResult.result'
        db.add_column(u'papers_analyzationresult', 'result',
                      self.gf('django.db.models.fields.TextField')(default=0),
                      keep_default=False)

        # Adding field 'AnalyzationResult.created'
        db.add_column(u'papers_analyzationresult', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2014, 3, 17, 0, 0), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'PaperComment'
        db.delete_table(u'papers_papercomment')


        # User chose to not deal with backwards NULL issues for 'AnalyzationResult.average_syllables_per_word'
        raise RuntimeError("Cannot reverse this migration. 'AnalyzationResult.average_syllables_per_word' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'AnalyzationResult.average_syllables_per_word'
        db.add_column(u'papers_analyzationresult', 'average_syllables_per_word',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'AnalyzationResult.text_length'
        raise RuntimeError("Cannot reverse this migration. 'AnalyzationResult.text_length' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'AnalyzationResult.text_length'
        db.add_column(u'papers_analyzationresult', 'text_length',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'AnalyzationResult.word_count'
        raise RuntimeError("Cannot reverse this migration. 'AnalyzationResult.word_count' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'AnalyzationResult.word_count'
        db.add_column(u'papers_analyzationresult', 'word_count',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'AnalyzationResult.total_syllables'
        raise RuntimeError("Cannot reverse this migration. 'AnalyzationResult.total_syllables' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'AnalyzationResult.total_syllables'
        db.add_column(u'papers_analyzationresult', 'total_syllables',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'AnalyzationResult.date_created'
        raise RuntimeError("Cannot reverse this migration. 'AnalyzationResult.date_created' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'AnalyzationResult.date_created'
        db.add_column(u'papers_analyzationresult', 'date_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'AnalyzationResult.percent_words_gt3_syllables'
        raise RuntimeError("Cannot reverse this migration. 'AnalyzationResult.percent_words_gt3_syllables' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'AnalyzationResult.percent_words_gt3_syllables'
        db.add_column(u'papers_analyzationresult', 'percent_words_gt3_syllables',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'AnalyzationResult.average_words_per_sentence'
        raise RuntimeError("Cannot reverse this migration. 'AnalyzationResult.average_words_per_sentence' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'AnalyzationResult.average_words_per_sentence'
        db.add_column(u'papers_analyzationresult', 'average_words_per_sentence',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'AnalyzationResult.words_gt3_syllables'
        raise RuntimeError("Cannot reverse this migration. 'AnalyzationResult.words_gt3_syllables' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'AnalyzationResult.words_gt3_syllables'
        db.add_column(u'papers_analyzationresult', 'words_gt3_syllables',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'AnalyzationResult.word_occurrence'
        raise RuntimeError("Cannot reverse this migration. 'AnalyzationResult.word_occurrence' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'AnalyzationResult.word_occurrence'
        db.add_column(u'papers_analyzationresult', 'word_occurrence',
                      self.gf('django.db.models.fields.TextField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'AnalyzationResult.sentence_count'
        raise RuntimeError("Cannot reverse this migration. 'AnalyzationResult.sentence_count' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'AnalyzationResult.sentence_count'
        db.add_column(u'papers_analyzationresult', 'sentence_count',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'AnalyzationResult.character_count'
        raise RuntimeError("Cannot reverse this migration. 'AnalyzationResult.character_count' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'AnalyzationResult.character_count'
        db.add_column(u'papers_analyzationresult', 'character_count',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)

        # Deleting field 'AnalyzationResult.result'
        db.delete_column(u'papers_analyzationresult', 'result')

        # Deleting field 'AnalyzationResult.created'
        db.delete_column(u'papers_analyzationresult', 'created')


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
            'stripe_customer_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'stripe_subscription_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'zip': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'})
        },
        u'papers.analyzationresult': {
            'Meta': {'object_name': 'AnalyzationResult'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paper': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['papers.Paper']"}),
            'result': ('django.db.models.fields.TextField', [], {})
        },
        u'papers.paper': {
            'Meta': {'ordering': "['-date_modified']", 'object_name': 'Paper'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.WUser']"})
        },
        u'papers.papercomment': {
            'Meta': {'object_name': 'PaperComment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.WUser']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paper': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['papers.Paper']"})
        },
        u'papers.papersubmission': {
            'Meta': {'ordering': "['-date_submitted']", 'object_name': 'PaperSubmission'},
            'date_submitted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paper': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['papers.Paper']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '350'}),
            'submitted_to': ('django.db.models.fields.EmailField', [], {'max_length': '75'})
        }
    }

    complete_apps = ['papers']