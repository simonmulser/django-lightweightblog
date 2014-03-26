from django.db import models
from django.utils import timezone
from django.core import validators
from django.utils.html import strip_tags


class Article (models.Model):
    #class Meta:
    #   abstract = True
    heading = models.CharField(validators=[validators.MinLengthValidator(2), validators.MaxLengthValidator(100)], max_length=100)
    content = models.TextField(validators=[validators.MinLengthValidator(10), validators.MaxLengthValidator(10000)])
    publication = models.DateTimeField()
    def is_published(self):
        return self.publication < timezone.now()

    def __unicode__(self):
        return self.heading
    
    def validate(self, value):
        self.heading.validate()
        
    def intro(self):
        return strip_tags(self.content)[:100]

