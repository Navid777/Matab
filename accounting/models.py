from django.db import models
from django.contrib import admin


class Account(models.Model):
    serial = models.IntegerField()
    credit = models.FloatField()

    def __unicode__(self):
        return "%04d%08d" % self.serial, self.id


class Document(models.Model):
    time = models.DateTimeField()
    description = models.CharField(max_length=300)
    resource_id = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.description[0:30] + "..."


class Record(models.Model):
    account = models.ForeignKey(Account)
    document = models.ForeignKey(Document)
    credit = models.FloatField()
    previous_credit = models.FloatField()
    next_credit = models.FloatField()
    description = models.CharField(max_length=300)

    def __unicode__(self):
        return self.account + ": " + self.description[0:20] + "..."


admin.site.register(Account)
admin.site.register(Document)
admin.site.register(Record)