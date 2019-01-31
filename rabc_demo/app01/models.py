from django.db import models

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=32)
    publish_date = models.DateField()
    author = models.ForeignKey('Author')

    def __unicode__(self):
        return self.title

class Author(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField()

    def __unicode__(self):
        return self.name