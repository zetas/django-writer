# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'EmailTemplate.type'
        db.add_column(u'main_emailtemplate', 'type',
                      self.gf('django.db.models.fields.CharField')(default='Accounts', max_length=50),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'EmailTemplate.type'
        db.delete_column(u'main_emailtemplate', 'type')


    models = {
        u'main.emailtemplate': {
            'Meta': {'object_name': 'EmailTemplate'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'html': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'verbose_name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['main']